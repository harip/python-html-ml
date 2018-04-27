import requests
from html.parser import HTMLParser
from queue  import Queue
import uuid
from stack import Stack

class HtmlTagInfo:
    def __init__(self,id,tag,tag_text,tag_val,attrs):
        self.id=id
        self.tag=tag
        self.tag_text=tag_text
        self.tag_val=tag_val
        self.attrs=attrs

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self,elements):
        HTMLParser.__init__(self)
        self.elements=elements
        
    def handle_starttag(self, tag, attrs):
        #id=self.get_id()
        #self.elements[id]=HtmlTagInfo("<",tag,None)
        self.elements.append("<" + tag)

    def handle_endtag(self, tag):
        #id=self.get_id()
        #self.elements[id]=HtmlTagInfo(">",tag,None)
        self.elements.append(">" + tag)

    def handle_data(self, data):
        #id=self.get_id()
        #self.elements[id]=HtmlTagInfo(None,None,data)
        self.elements.append(data)

    def get_id(self):
        return str(uuid.uuid4())


dom=requests.get("https://www.google.com/")
mappings = []
parser = MyHTMLParser(mappings)
parser.feed(dom.text)

print(mappings)