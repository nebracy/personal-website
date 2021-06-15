from datetime import datetime
import pytest
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
    pass


@pytest.mark.parametrize("dt, expected_dt",
                         [(datetime(2021, 4, 26, 10, 27, 16), datetime(2021, 4, 26, 6, 27, 16)),
                          (datetime(2022, 1, 2, 0, 0), datetime(2022, 1, 1, 19, 0))])
def test_convert_tz(dt, expected_dt):
    """GithubCommits method converts naive utc datetime to aware etc datetime"""
    converted = GithubCommits.convert_tz(dt)
    expected = pytz.timezone('US/Eastern').localize(expected_dt)
    assert expected == converted


