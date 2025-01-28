import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)        
        self.assertEqual(node, node2)        

    def test_text(self):
        node = TextNode("This is a text node", TextType.BOLD)        
        node2 = TextNode("This is not equal", TextType.NORMAL)        
        self.assertNotEqual(node, node2)

    def test_text_type(self):
        node = TextNode("This is a text node", TextType.NORMAL, "https://www.boot.dev")        
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")                
        self.assertNotEqual(node, node2)                

    def test_url(self):
        node = TextNode("This is a text node", TextType.NORMAL, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.NORMAL, "http://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertEqual("TextNode(This is a text node, bold, https://www.boot.dev)", repr(node))

if __name__ == "__main__":
    unittest.main()