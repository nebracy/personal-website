import os
from github import Github
import pytz
from sqlalchemy import event
from nebracy import db

github = Github(os.getenv('GITHUB_TOKEN'))


class Commit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commit_id = db.Column(db.String(40), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    msg = db.Column(db.String(75), nullable=False)

    def __init__(self, commit_id, name, url, date, msg):
        self.commit_id = commit_id
        self.name = name
        self.url = url
        self.date = date
        self.msg = msg

    def __repr__(self):
        return f'<Commit {self.commit_id}, {self.name}, {self.date}, {self.msg}>'


@event.listens_for(Commit.__table__, 'after_create')
def main(*args, **kwargs):
    recent = get_recent_commits(5)
    add_initial_commits(recent)


def get_recent_commits(num):
    commit_list = []
    for repo in github.get_user().get_repos():
        commits = repo.get_commits()[:num]
        for c in commits:
            repo_name = repo.full_name
            repo_url = repo.html_url
            commit_msg = c.commit.message
            commit_date = convert_tz(c.commit.committer.date)
            commit_id = c.commit.sha
            commit_info = {'id': commit_id, 'name': repo_name, 'url': repo_url, 'date': commit_date, 'msg': commit_msg}
            commit_list.append(commit_info)
    final_list = sorted(commit_list, key=lambda commit: commit['date'], reverse=True)
    return final_list[:num]


def convert_tz(date):
    utc_date = pytz.utc.localize(date)
    est_date = utc_date.astimezone(pytz.timezone('America/New_York'))
    return est_date


def add_initial_commits(commits):
    for commit in commits:
        c = Commit(commit['id'], commit['name'], commit['url'], commit['date'], commit['msg'])
        db.session.add(c)
    db.session.commit()
