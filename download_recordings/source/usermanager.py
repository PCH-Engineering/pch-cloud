import requests
import pprint
import server_paths as url

def login(host, username='demo', password='password', ):

    # login and get token 
    r = requests.post(url.usermanager(host)+"/login", data={'username': username, 'password': password}, verify=False)
    print("login status", r.status_code, r.reason)

    if r.status_code != requests.codes.created:
        print('login failed')
        return
    session = r.json()
    return session

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)
    session = login('pchcloud', 'demo', 'password')
    pp.pprint(session)
    