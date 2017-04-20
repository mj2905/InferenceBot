import requests
from bs4 import BeautifulSoup

user = 'testbot'
passw = 'dhbot2017'
baseurl = 'http://wikipast.epfl.ch/wikipast/'
summary = 'Wikipastbot update'
names = ['bacasable']


def run():
    establish_connexion()

    for name in names:
        result = requests.post(baseurl + 'api.php?action=query&titles=' + name + '&export&exportnowrap')
        soup = BeautifulSoup(result.text, "lxml")
        # soup=BeautifulSoup(result.text)
        code = ''
        for primitive in soup.findAll("text"):
            code += primitive.string
        print(code)


def establish_connexion():
    # Login request
    payload = {'action': 'query', 'format': 'json', 'utf8': '', 'meta': 'tokens', 'type': 'login'}
    r1 = requests.post(baseurl + 'api.php', data=payload)

    # login confirm
    login_token = r1.json()['query']['tokens']['logintoken']
    payload = {'action': 'login', 'format': 'json', 'utf8': '', 'lgname': user, 'lgpassword': passw,
               'lgtoken': login_token}
    r2 = requests.post(baseurl + 'api.php', data=payload, cookies=r1.cookies)

    # get edit token2
    params3 = '?format=json&action=query&meta=tokens&continue='
    r3 = requests.get(baseurl + 'api.php' + params3, cookies=r2.cookies)
    edit_token = r3.json()['query']['tokens']['csrftoken']

    edit_cookie = r2.cookies.copy()
    edit_cookie.update(r3.cookies)


if __name__ == '__main__':
    run()
