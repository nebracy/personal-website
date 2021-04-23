from nebracy.models import Commit
from datetime import datetime


def test_commit_class(client):
    date = datetime.strptime('2021-04-20 13:27:16', '%Y-%m-%d %H:%M:%S')
    commit = Commit('778df45a6d', 'nebracy/personal-website', 'https://github.com/nebracy/personal-website', date, 'Test commit message')
    assert commit.name == 'nebracy/personal-website'


def test_query_order_limit(client):
    commit = Commit.query.order_by(Commit.date.desc()).limit(3).all()
    assert len(commit) == 3
    # check commits from most recent
