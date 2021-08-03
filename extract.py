import requests
import json

MY_TOKEN = 'abc123xyz'
MY_REPO = 'parasutcom/da-vinci'
TOTAL_CLOSED_PRS = 1094

url = 'https://api.github.com/repos/' + MY_REPO + '/pulls?state=closed&per_page=25'

headers = {"Authorization": "token " + MY_TOKEN}

closed_prs = {}
page = 1

while len(closed_prs) <= TOTAL_CLOSED_PRS:
    prs = requests.get(url + '&page=' + str(page), headers=headers).text
    prs = json.loads(prs)
    for pr in prs:
        new_pr = { pr['id']: {'title': pr['title'], 'comments_url': pr['comments_url'] } }
        closed_prs.update(new_pr)
    print(len(closed_prs))
    page = page + 1
    print(page)

for pr_id in closed_prs.keys():
    pr = closed_prs[pr_id]
    url = pr['comments_url']
    request = requests.get(url, headers=headers)
    if '@dependabot ignore this dependency' in request.text:
        print('Aha')
        print(url)
        print(pr['title'])
