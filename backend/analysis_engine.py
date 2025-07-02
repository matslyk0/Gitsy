import requests

# repository URLs will be pasted in the format https://github.com/{owner}/{repo}

def get_commits(repo_url):

    # isolating the {owner}/{repo} and stitching it with the API endpoint
    info = repo_url.removeprefix("https://github.com/")
    url = f"https://api.github.com/repos/{info}/commits"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error in retrieving data. Status code {response.status_code}"

repo_info = get_commits("https://github.com/matslyk0/Gitsy")
print(repo_info)
