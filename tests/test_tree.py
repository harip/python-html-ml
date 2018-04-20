# https://github.com/harip/python-data-structures
from tree_ds import *

def test_tree_get_node():
    t=Tree()

    # Add a parent node
    n=NodeInfo("Html",None,NodeType.ROOT)
    t.add_node(n,None)

    # Add a child node
    cn=NodeInfo("head",None,None)
    t.add_node(cn,n)

    node=t.get_node("head")

    assert node.node_key=="head","head node should be returned"