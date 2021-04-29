from datetime import datetime
import os
import pytest
from nebracy.models import Commit, GithubCommits


def test_commit_class(client):
    date = datetime.strptime('2021-04-20 13:27:16', '%Y-%m-%d %H:%M:%S')
    commit = Commit('778df45a6d', 'nebracy/personal-website', 'https://github.com/nebracy/personal-website', date, 'Test commit message')
    assert commit.name == 'nebracy/personal-website'


# def test_query_order_limit(client):       TODO fails for now, update
#     commit = Commit.query.order_by(Commit.date.desc()).limit(3).all()
#     assert len(commit) == 3
#     # check commits from most recent


# def test_missing_github_env_except(monkeypatch, client):
#     """"""
#     monkeypatch.delenv('GITHUB_TOKEN')


"""test fill empty list with 3 commits per repo from github - MOCK: github api RETURN repo"""


"""test narrow list to most recent 3"""


"""test no commits older than 6 months in list"""

