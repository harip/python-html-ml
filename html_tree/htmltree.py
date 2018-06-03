import sys, os
import requests
from html.parser import HTMLParser
from queue  import Queue
import uuid
from stack import Stack
from collections import OrderedDict
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from tree_ds import *

class HtmlNodeInfo:
    def __init__(self, key, index, data):
        self.key = key
        self.index = index
        self.data = data

class HtmlNode:
    def __init__(self, start, data, id, parent_id):
        self.start = start
        self.data = data
        self.id = id
        self.parent_id = parent_id

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self, elements, node_id):
        HTMLParser.__init__(self)
        self.elements = elements
        self.node_id = node_id

    def handle_starttag(self, tag, attrs):
        key=f'<{tag}'
        self.elements.append( HtmlNodeInfo(key,self.node_id,attrs))
        self.node_id=self.node_id+1    

        if (    tag.lower()=="link" or 
                tag.lower()=="meta" or 
                tag.lower()=="br" or 
                tag.lower()=="img" or
                tag.lower()=="input"
        ):
            #There is no end, so lets add one
            key=f'>'
            self.elements.append( HtmlNodeInfo(key,self.node_id,attrs))
            # print("Encountered a end tag:" + tag + "," + str(self.node_id))
            self.node_id=self.node_id+1       

    def handle_endtag(self, tag):

        if (    tag.lower()=="link" or 
                tag.lower()=="meta" or 
                tag.lower()=="br" or 
                tag.lower()=="img" or
                tag.lower()=="input"
        ):
            return

        key=f'>'
        self.elements.append( HtmlNodeInfo(key,self.node_id,None))       
        self.node_id=self.node_id+1

    def handle_data(self, data):
        self.elements.append( HtmlNodeInfo("",self.node_id,data))
        self.node_id=self.node_id+1

    def handle_startendtag(self, tag, attrs):
        # for <meta />        
        key=f'<{tag}'
        self.elements.append( HtmlNodeInfo(key,self.node_id,attrs))
        self.node_id=self.node_id+1    

        key=f'>'
        self.elements.append( HtmlNodeInfo(key,self.node_id,attrs))       
        self.node_id=self.node_id+1

    def get_elements(self):
        return self.elements

dom=requests.get("https://nyctf.tt2beta.org/")
mappings = []
parser = MyHTMLParser(mappings,0)
dom_text=dom.text

# dom_text='<meta property="og:site_name" content="Yahoo" >'
parser.feed(dom_text)
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
        data_node=[]
        if (elem.index-pop_elem.index)>1:
            # The data for this element is in between elem and pop_elem
            # however filter for data is not None
            datas_nodes=elements[pop_elem.index+1:elem.index]
            data_node=[dn for dn in datas_nodes if dn.data is not None]
        data=None if len(data_node)==0 else data_node[0]

        if stack.is_empty():
            parent_elem_index=pop_elem.index 
        else:
            parent_elem_index=stack.peek().index  
        
        key=f'{pop_elem.key}{elem.key}'
        node=HtmlNode(key,data,pop_elem.index,parent_elem_index)  
        final_list.append(node)
 

final_list=sorted(final_list,key=lambda p: (p.parent_id,p.id))
# pprint( "item_id,parent_id,item" )
# for item in final_list:
#     pprint( str(item.id) + "," + str(item.parent_id) + "," + item.start )

t=Tree()
n=NodeInfo(final_list[0].start,None,NodeType.ROOT,f'{final_list[0].start}_{final_list[0].id}') 
t.add_node(n,None)

for item in final_list:
    # Get this items parent
    parent= next(p for p in final_list if p.id==item.parent_id)
    uniq_name=f'{parent.start}_{parent.id}'
    parent_node= t.get_node_by_uniq(uniq_name)

    # Create child node
    cn_uniq_name=f'{item.start}_{item.id}'
    
    node_data=""
    if item.data is not None:
        node_data=item.data.data
    cn=NodeInfo(item.start,node_data,None,cn_uniq_name) 

    # Add to tree
    t.add_node(cn,parent_node)

# t.plot_paths()
# t.plot_tree({})
t.plot_tree_v2({})
# t.export_tree_tocsv("nyctf.csv")