from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def text_node_to_html_node(text_node:TextNode):    
    match text_node.text_type:
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINKS:
            if text_node.url is None:
                raise ValueError("Invalid HTML: TextNode is missing URL")
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGES:
            if text_node.url is None:
                raise ValueError("Invalid HTML: TextNode is missing URL")
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Invalid HTML: Unrecognized TextNode type")
        
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
    #print(node)
    #print(htmlnode)
    #print(leafnode.to_html())
    #print(parent.to_html())
    #print(parent2.to_html())

main()