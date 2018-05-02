import requests
from html.parser import HTMLParser
from queue  import Queue
import uuid
from stack import Stack
from collections import OrderedDict

class HtmlTagInfo:
    def __init__(self,id,tag,tag_text,tag_val,attrs):
        self.id=id
        self.tag=tag
        self.tag_text=tag_text
        self.tag_val=tag_val
        self.attrs=attrs

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self,elements,node_id):
        HTMLParser.__init__(self)
        self.elements=elements
        self.node_id=node_id 
        
    def handle_starttag(self, tag, attrs):
        key=f'< {str(self.node_id)} {tag}'
        self.elements.append( HtmlNodeInfo(key,self.node_id+1,None))
        self.node_id=self.node_id+1

    def handle_endtag(self, tag):
        key=f'> {str(self.node_id)} {tag}'
        self.elements.append( HtmlNodeInfo(key,self.node_id+1,None))
        self.node_id=self.node_id+1

    def handle_data(self, data):
        self.elements.append( HtmlNodeInfo(None,self.node_id+1,None))
        self.node_id=self.node_id+1

    def get_elements(self):
        return self.elements


dom=requests.get("https://www.google.com/")
# mappings = OrderedDict()
mappings = []
parser = MyHTMLParser(mappings,0)
parser.feed(dom.text)

elements=parser.get_elements()
# print(elements)


stack=Stack()
for elem in elements:
    if elem.startswith("<"):
        stack.push(elem)
    
    if elem.startswith(">"):
        # Closing tag
        # Pop the first item from stack
        pop_elem=stack.pop()

        # Get the data
        pop_elem_data=stack.peek
        pop_elem_data_key=f'{pop_elem_key}_data'
        pop_elem_start_Key=f'{pop_elem'

        print(pop_elem)
        print(elem)
        break


class HtmlNodeInfo:
    def __init__(self,key,index,data):
        self.key=key
        self.index=index
        self.data=data

class HtmlNode:
    def __init__(self,start,end,data):
        self.start=start
        self.end=end
        self.data=data