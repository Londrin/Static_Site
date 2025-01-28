import unittest

from htmlnode import LeafNode
from textnode import TextType, TextNode
from main import text_node_to_html_node

class TestTextConversion(unittest.TestCase):
    def test_type_conversion(self):
        normal = TextNode("This is normal", TextType.NORMAL)
        bold = TextNode("This is bold", TextType.BOLD)
        italic = TextNode("This is italic", TextType.ITALIC)
        code = TextNode("This is code", TextType.CODE)
        image = TextNode("This image is beautiful", TextType.IMAGES, "https://image.boot.dev")
        link = TextNode("Go here", TextType.LINKS, "https://www.boot.dev")

        self.assertEqual(text_node_to_html_node(normal), LeafNode(None, normal.text))
        self.assertEqual(text_node_to_html_node(bold), LeafNode("b", bold.text))
        self.assertEqual(text_node_to_html_node(italic), LeafNode("i", italic.text))
        self.assertEqual(text_node_to_html_node(code), LeafNode("code", code.text))
        self.assertEqual(text_node_to_html_node(image), LeafNode("img", "", {"src": image.url, "alt": image.text}))
        self.assertEqual(text_node_to_html_node(link), LeafNode("a", link.text, {"href": link.url}))       

    def test_type_no_url(self):
        image = TextNode("This image is beautiful", TextType.IMAGES, None)
        link = TextNode("Go here", TextType.LINKS, None)
        with self.assertRaises(Exception):
            text_node_to_html_node(image)
        with self.assertRaises(Exception):
            text_node_to_html_node(link)


if __name__ == "__main__":
    unittest.main()
