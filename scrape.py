import pprint
import requests
from bs4 import BeautifulSoup


res = requests.get('https://news.ycombinator.com/news')
res_2 = requests.get('https://news.ycombinator.com/news?p=2')
res_3 = requests.get('https://news.ycombinator.com/news?p=3')

soup = BeautifulSoup(res.text, 'html.parser')
soup_2 = BeautifulSoup(res_2.text, 'html.parser')
soup_3 = BeautifulSoup(res_3.text, 'html.parser')

links = soup.select('.titleline')
links_2 = soup_2.select('.titleline')
links_3 = soup_3.select('.titleline')

subtext = soup.select('.subtext')
subtext_2 = soup_2.select('.subtext')
subtext_3 = soup_3.select('.subtext')

mega_links = links + links_2 + links_3
mega_subtext = subtext + subtext_2 + subtext_3


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k:k['votes'], reverse=True)


def create_custom_hn(hnlink, hnsubtext):
    hn = []
    for idx, item in enumerate(hnlink):
        title = item.getText()
        href = item.a.get('href', None)
        vote = hnsubtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ' '))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)

pprint.pprint(create_custom_hn(mega_links, mega_subtext))
