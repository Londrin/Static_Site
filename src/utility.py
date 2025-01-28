from textnode import TextNode, TextType
from htmlnode import LeafNode
import re

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
        
def split_nodes_delimiter(old_nodes:list[TextNode], delimiter, text_type:TextType):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.NORMAL:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception("Invalid Markdown: Missing delimiter")
            for i in range(len(split_text)):
                if split_text[i] == "":
                    continue
                if i %2 == 0:
                    new_nodes.append(TextNode(split_text[i], TextType.NORMAL))
                else:
                    new_nodes.append(TextNode(split_text[i], text_type))
        else:
            new_nodes.append(node)

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
