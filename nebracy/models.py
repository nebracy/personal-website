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


# TODO limit commits retrieved per repo to within the last 6 months
# TODO also need message on website when there are no recent commits/table is empty
def add_initial_commits(commits):
    for commit in commits:
        c = Commit(commit['id'], commit['name'], commit['url'], commit['date'], commit['msg'])
        db.session.add(c)
    db.session.commit()


def convert_tz(date):
    utc_date = pytz.utc.localize(date)
    est_date = utc_date.astimezone(pytz.timezone('America/New_York'))
    return est_date


def get_commits_per_repo(num):
    commit_list = []
    for repo in github.get_user().get_repos():
        commits = repo.get_commits()[:num]
        for c in commits:               # add check for commit_date < 6 mo from today
            commit_date = convert_tz(c.commit.committer.date)
            commit_list.append({'id': c.commit.sha, 'name': repo.full_name, 'url': repo.html_url,
                                'date': commit_date, 'msg': c.commit.message})
    final_list = sorted(commit_list, key=lambda commit: commit['date'], reverse=True)
    return final_list[:num]


@event.listens_for(Commit.__table__, 'after_create')
def autofill_commit_table(*args, **kwargs):
    recent = get_commits_per_repo(3)
    add_initial_commits(recent)
