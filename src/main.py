from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utility import *
        
def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    my_dict = {"href": "https://www.google.com", "target": "_blank"}

    htmlnode = HTMLNode("a", "b", [HTMLNode("p"), HTMLNode("h1")], my_dict)

    leafnode = LeafNode("a", "value", my_dict)
    parent = ParentNode("p", 
                        [LeafNode("b", "Bold text"),
                         LeafNode(None, "Normal text"),
                         LeafNode("i", "italic text"),
                         LeafNode(None, "Normal text"),
                         ParentNode("p", 
                                    [LeafNode("b", "Bold text"),
                         LeafNode(None, "Normal text"),
                         LeafNode("i", "italic text"),
                         LeafNode(None, "Normal text")])])
    parent2 = ParentNode("p", None)
    node = TextNode(
    "Start ![first](img1.jpg) middle ![second](img2.jpg) end",
    TextType.NORMAL
    )
    result = split_nodes_image([node])
    print(result)

    node = TextNode(
    "Start [first](img1.jpg) middle [second](img2.jpg) end",
    TextType.NORMAL
    )
    result = split_nodes_link([node])
    print(result)
    #print(node)
    #print(htmlnode)
    #print(leafnode.to_html())
    #print(parent.to_html())
    #print(parent2.to_html())

main()