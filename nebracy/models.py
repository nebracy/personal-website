import os
from github import Github
import pytz
from sqlalchemy import event
from nebracy import db
from dateutil.relativedelta import relativedelta
from datetime import datetime


class Commit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commit_id = db.Column(db.String(40), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    msg = db.Column(db.String(75), nullable=False)
    github = Github(os.getenv('GITHUB_TOKEN'))

    def __init__(self, commit_id=None, name=None, url=None, date=None, msg=None):
        self.commit_id = commit_id
        self.name = name
        self.url = url
        self.date = date
        self.msg = msg
        self.commit_list = []

    def __repr__(self):
        return f'<Commit {self.commit_id}, {self.name}, {self.url}, {self.date}, {self.msg}>'

    def __len__(self):
        return len(self.commit_list)

    def get_commits_per_repo(self, num, months_ago=6):
        num_months_ago = datetime.today() - relativedelta(months=months_ago)
        for repo in Commit.github.get_user().get_repos():
            commits = repo.get_commits()[:num]
            for c in commits:
                if c.commit.committer.date > num_months_ago:
                    commit_date = self.convert_tz(c.commit.committer.date)
                    self.commit_list.append({'id': c.commit.sha, 'name': repo.full_name, 'url': repo.html_url,
                                            'date': commit_date, 'msg': c.commit.message})

    def add_initial_commits(self):
        for commit in self.commit_list:
            c = Commit(commit['id'], commit['name'], commit['url'], commit['date'], commit['msg'])
            db.session.add(c)
        db.session.commit()

    def convert_tz(self, unconverted_date):
        utc_date = pytz.utc.localize(unconverted_date)
        est_date = utc_date.astimezone(pytz.timezone('America/New_York'))
        return est_date

    def sort_list(self, num):
        final_list = sorted(self.commit_list, key=lambda commit: commit['date'], reverse=True)[:3]
        self.commit_list = final_list[:num]


@event.listens_for(Commit.__table__, 'after_create')
def autofill_table(*args, **kwargs):
    commit = Commit()
    max_num = 3
    commit.get_commits_per_repo(max_num)
    commit.sort_list(max_num)
    commit.add_initial_commits()



