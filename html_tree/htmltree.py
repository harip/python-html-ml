import requests
from html.parser import HTMLParser
from queue  import Queue
import uuid
from collections import OrderedDict

class HtmlTagInfo:
    def __init__(self,tag,tag_text,tag_val):
        self.tag=tag
        self.tag_text=tag_text
        self.tag_val=tag_val

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self,elements):
        HTMLParser.__init__(self)
        self.elements=elements

    def handle_starttag(self, tag, attrs):
        id=self.get_id()
        self.elements[id]=HtmlTagInfo("<",tag,None)

    def handle_endtag(self, tag):
        id=self.get_id()
        self.elements[id]=HtmlTagInfo(">",tag,None)

    def handle_data(self, data):
        id=self.get_id()
        self.elements[id]=HtmlTagInfo(None,None,data)

    def get_id(self):
        return str(uuid.uuid4())


dom=requests.get("https://www.google.com/")
mappings = OrderedDict()
parser = MyHTMLParser(mappings)
parser.feed(dom.text)

elements=parser.elements
print(elements)