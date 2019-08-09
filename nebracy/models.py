import os
from sqlalchemy import event
from github import Github
from nebracy import db

github = Github(os.getenv('GITHUB_TOKEN'))


class Commit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    msg = db.Column(db.String(75), nullable=False)

    def __init__(self, name, url, date, msg):
        self.name = name
        self.url = url
        self.date = date
        self.msg = msg

    def __repr__(self):
        return f'<Commit {self.name}, {self.date}, {self.msg}>'


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
            commit_date = c.commit.committer.date
            commit_info = {'name': repo_name, 'url': repo_url, 'msg': commit_msg, 'date': commit_date}
            commit_list.append(commit_info)
    final_list = sorted(commit_list, key=lambda commit: commit['date'], reverse=True)
    return final_list[:num]


def add_initial_commits(commits):
    for commit in commits:
        c = Commit(commit['name'], commit['url'], commit['date'], commit['msg'])
        db.session.add(c)
    db.session.commit()
