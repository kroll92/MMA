import requests
from bs4 import BeautifulSoup


def scrape_fighters():
    url = 'http://ufc.com/rankings'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    fighters = []
    for row in soup.select('.view-rankings tr'):
        columns = row.select('td')
        if len(columns) > 1:
            rank = columns[0].text.strip()
            fighter = columns[1].text.strip()
            fighters.append((rank, fighter))

    return fighters


# Wywołujemy funkcję i drukujemy wyniki
fighters = scrape_fighters()
for rank, fighter in fighters:
    print(rank, fighter)