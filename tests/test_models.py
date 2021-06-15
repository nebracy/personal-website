from datetime import datetime
import pytz
from nebracy.models import Commit, GithubCommits


def test_commit_class(client):
    """"""
    date = datetime.strptime('2021-04-20 13:27:16', '%Y-%m-%d %H:%M:%S')
    commit = Commit('778df45a6d', 'nebracy/personal-website', 'https://github.com/nebracy/personal-website', date, 'Test commit message')
    assert commit.name == 'nebracy/personal-website'


# def test_query_order_limit(client):       TODO update test, currently fails
#     """"""
#     commit = Commit.query.order_by(Commit.date.desc()).limit(3).all()
#     assert len(commit) == 3
#     # check commits from most recent


# def test_missing_github_env_except(monkeypatch, client):
#     """"""
#     monkeypatch.delenv('GITHUB_TOKEN')


def test_a():
    """test fill empty list with 3 commits per repo from github - MOCK: github api RETURN repo"""
    pass


def test_b():
    """test narrow list to most recent 3"""
    pass


def test_c():
    """test no commits older than 6 months in list"""


def test_convert_tz():
    """test GithubCommits method converts naive utc datetime to etc datetime"""
    dt = datetime.strptime('2021-04-26 10:27:16', '%Y-%m-%d %H:%M:%S')
    converted = GithubCommits.convert_tz(dt)
    expected = pytz.timezone('US/Eastern').localize(datetime(2021, 4, 26, 6, 27, 16, 0))
    assert expected == converted


