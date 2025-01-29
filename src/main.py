from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utility import *
        
def main():
    text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    print(text_to_textnodes(text))

main()