import os
from github import Github
import pytz
from sqlalchemy import event
from nebracy import db
from dateutil.relativedelta import relativedelta
from datetime import datetime


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
    github = Github(os.getenv('GITHUB_TOKEN'))

    def __init__(self, commit_num=3):
        self.commit_num = commit_num
        self.list = []
        self.commit = Commit

    def __repr__(self):
        return f'<GithubCommits {self.commit_num}>'

    def __len__(self):
        return len(self.list)

    def get_commits_per_repo(self, months_ago=6):
        num_months_ago = datetime.today() - relativedelta(months=months_ago)
        for repo in GithubCommits.github.get_user().get_repos():
            commits = repo.get_commits()[:self.commit_num]
            for c in commits:
                if c.commit.committer.date > num_months_ago:
                    commit_date = self.convert_tz(c.commit.committer.date)
                    self.list.append({'id': c.commit.sha, 'name': repo.full_name, 'url': repo.html_url,
                                      'date': commit_date, 'msg': c.commit.message})

    @staticmethod
    def convert_tz(unconverted_date):
        utc_date = pytz.utc.localize(unconverted_date)
        est_date = utc_date.astimezone(pytz.timezone('America/New_York'))
        return est_date

    def sort_list(self):
        final_list = sorted(self.list, key=lambda commit: commit['date'], reverse=True)[:3]
        self.list = final_list[:self.commit_num]

    def add_to_db(self, payload=None):
        if payload is not None:
            self.process_webhook(payload)
        for commit in self.list:
            c = self.commit(commit['id'], commit['name'], commit['url'], commit['date'], commit['msg'])
            db.session.add(c)
        db.session.commit()

    def process_webhook(self, payload):
        for commit in payload['commits']:
            self.list.append({'id': commit['id'], 'name': payload['repository']['name'],
                              'url': payload['repository']['url'],
                              'date': datetime.fromisoformat(commit['timestamp']), 'msg': commit['message']})


@event.listens_for(Commit.__table__, 'after_create')
def autofill_table(*args, **kwargs):
    github_commits = GithubCommits()
    github_commits.get_commits_per_repo()
    github_commits.sort_list()
    github_commits.add_to_db()



