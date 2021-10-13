import os
import pytz
from datetime import datetime
from dateutil.relativedelta import relativedelta
from github import Github, GithubException
from sqlalchemy import event
from typing import Optional
from nebracy import db


class Commit(db.Model):
    __tablename__ = 'commit'
    id = db.Column(db.Integer, primary_key=True)
    commit_id = db.Column(db.String(40), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    msg = db.Column(db.String(75), nullable=False)

    def __init__(self, commit_id=None, name=None, url=None, date=None, msg=None):
        self.commit_id = commit_id
        self.name = name
        self.url = url
        self.date = date
        self.msg = msg

    def __repr__(self):
        return f'<Commit {self.commit_id}, {self.name}, {self.url}, {self.date}, {self.msg}>'


class GithubCommits:
    __tablename__ = 'github commits'

    def __init__(self, commit_num: int = 3) -> None:
        self.commit_num = commit_num
        self.list = []
        self.commit = Commit

    def __repr__(self) -> str:
        return f'<GithubCommits {self.commit_num}>'

    def __len__(self) -> int:
        return len(self.list)

    def get_commits_per_repo(self, github_token, months_ago: int = 6) -> None:
        num_months_ago = datetime.today() - relativedelta(months=months_ago)
        for repo in github_token.get_user().get_repos():
            commits = repo.get_commits()[:self.commit_num]
            for c in commits:
                if c.commit.committer.date > num_months_ago:
                    self.list.append({'id': c.commit.sha, 'name': repo.full_name, 'url': repo.html_url,
                                      'date': self.convert_tz(c.commit.committer.date), 'msg': c.commit.message})

    def sort_list(self) -> None:
        final_list = sorted(self.list, key=lambda commit: commit['date'], reverse=True)[:3]
        self.list = final_list[:self.commit_num]

    def add_to_db(self, payload: Optional[dict] = None) -> None:
        if payload is not None:
            self.process_webhook(payload)
        for commit in self.list:
            c = self.commit(commit['id'], commit['name'], commit['url'], commit['date'], commit['msg'])
            db.session.add(c)
        db.session.commit()

    def process_webhook(self, payload: dict) -> None:
        for commit in payload['commits']:
            self.list.append({'id': commit['id'], 'name': payload['repository']['full_name'],
                              'url': payload['repository']['url'],
                              'date': datetime.fromisoformat(commit['timestamp']), 'msg': commit['message']})

    @staticmethod
    def convert_tz(unconverted_date: datetime) -> datetime:
        utc_date = pytz.utc.localize(unconverted_date)
        est_date = utc_date.astimezone(pytz.timezone('US/Eastern'))
        return est_date


class GithubTokenNotFoundError(Exception):
    pass


@event.listens_for(Commit.__table__, 'after_create')
def autofill_table(*args, **kwargs) -> None:
    github_commits = GithubCommits()
    try:
        github_commits.get_commits_per_repo(Github(os.getenv('GITHUB_TOKEN')))
    except GithubException as e:
        print(e)
        raise GithubTokenNotFoundError("The environment variable GITHUB_TOKEN is not set")
    else:
        github_commits.sort_list()
        github_commits.add_to_db()




