import requests
from html.parser import HTMLParser
from queue  import Queue
import uuid
from stack import Stack
from collections import OrderedDict
from pprint import pprint

class HtmlNodeInfo:
    def __init__(self,key,index,data):
        self.key=key
        self.index=index
        self.data=data

class HtmlNode:
    def __init__(self,start,data,id,parent_id):
        self.start=start
        self.data=data        
        self.id=id
        self.parent_id=parent_id

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self,elements,node_id):
        HTMLParser.__init__(self)
        self.elements=elements
        self.node_id=node_id 
        
    def handle_starttag(self, tag, attrs):
        key=f'<{tag}'
        self.elements.append( HtmlNodeInfo(key,self.node_id+1,None))
        self.node_id=self.node_id+1

    def handle_endtag(self, tag):
        key=">"
        self.elements.append( HtmlNodeInfo(key,self.node_id+1,None))
        self.node_id=self.node_id+1

    def handle_data(self, data):
        self.elements.append( HtmlNodeInfo("",self.node_id+1,data))
        self.node_id=self.node_id+1

    def get_elements(self):
        return self.elements


dom=requests.get("https://www.google.com/")
# mappings = OrderedDict()
mappings = []
parser = MyHTMLParser(mappings,0)
parser.feed(dom.text)

elements=parser.get_elements()
final_list=[]
stack=Stack()
for elem in elements:
    if elem.key.startswith("<"):
        stack.push(elem)
    
    if elem.key.startswith(">"):
        # Closing tag
        # Pop the first item from stack
        pop_elem=stack.pop()

        # Get the data
        data_index=elem.index-2
        data_node=elements[data_index]

        # Get the parent id
        parent_index=pop_elem.index-2
        parent_elem=elements[parent_index]

        key=f'{pop_elem.key}{elem.key}'
        node=HtmlNode(key,data_node.data,parent_elem.index,parent_index)  
        final_list.append(node)

for item in final_list:
    pprint( str(item.id) + "," + str(item.parent_id) + "," + item.start )


