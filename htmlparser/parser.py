import requests

def get_page(url):
    dom=requests.get(url)
    print(dom.text)

if __name__=="__main__":
    get_page("https://www.google.com/")