import requests
from bs4 import BeautifulSoup

user = 'InferenceBot'
passw = 'praisekek'
baseurl = 'http://wikipast.epfl.ch/wikipast/'
summary = 'Wikipastbot update'
listPage = 'InferenceBot - Listes des pages de test'
writePage = 'InferenceBot - Output'



def write_on_page(text, page = writePage):
    (edit_token, edit_cookie) = establish_connexion()
    
    payload = {'action':'edit','assert':'user','format':'json','utf8':'','text':text,'summary':summary,'title':page,'token':edit_token}
    r4=requests.post(baseurl+'api.php',data=payload,cookies=edit_cookie)
    print("Finished writing")


def run():
    establish_connexion()
    
    result = requests.post(baseurl + 'api.php?action=query&titles=' + listPage + '&export&exportnowrap')
    soup = BeautifulSoup(result.text, "lxml")
    print(soup)


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
    
    return(edit_token, edit_cookie)


if __name__ == '__main__':
    run()
