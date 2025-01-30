from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utility import *
from markdown import *
        
def main():
    text = "# This is a heading\n\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item\n\n\n\n\n\n\n\n\n"
    result = markdown_to_html_node(text)
    print(result)

main()