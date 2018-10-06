import os
from datetime import datetime
from github import Github

g = Github(os.environ['GITHUB_TOKEN'])


def get_recent_commits(num):
    commit_list = []
    for repository in g.get_user().get_repos():
        repo = g.get_user('nebracy').get_repo(name=repository.name)
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


if __name__ == "__main__":

    def format_commits(comm):
        for commit in comm:
            name = commit['name']
            url = commit['url']
            msg = commit['msg']
            date = datetime.strftime(commit['date'], '%b. %d, %Y')
            print(name, url, msg, date)

    recent = get_recent_commits(5)
    format_commits(recent)
