from enum import Enum

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type:TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node):
        if not isinstance(self, TextNode) and not isinstance(node, TextNode):
            return False
        if self.text == node.text and self.text_type == node.text_type and self.url == node.url:
            return True
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
