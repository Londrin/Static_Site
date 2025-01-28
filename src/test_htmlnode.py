import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        my_dict = {"href": "https://www.google.com", "target": "_blank"}    
        node = HTMLNode("a", "b", [HTMLNode("p"), HTMLNode("h1")], my_dict)
        self.assertEqual(" href=\"https://www.google.com\" target=\"_blank\"", node.props_to_html())
    
    def test_repr(self):
        my_dict = {"href": "https://www.google.com", "target": "_blank"}    
        node = HTMLNode("a", "b", [HTMLNode("p"), HTMLNode("h1")], my_dict)
        self.assertEqual("HTMLNode(a, b, [HTMLNode(p, None, None, None), HTMLNode(h1, None, None, None)], {'href': 'https://www.google.com', 'target': '_blank'})", repr(node))

    def test_to_html_error(self):
        node = HTMLNode("a")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_members(self):
        node = LeafNode("a", "This is a value")
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "This is a value")
        self.assertEqual(node.props, None)
    
    def test_to_html(self):
        node = LeafNode("a", "value", {"href": "https://www.boot.dev", "class": "greeting"})
        node2 = LeafNode("a", "value")
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev" class="greeting">value</a>')
        self.assertEqual(node2.to_html(), "<a>value</a>")

    def test_to_html_check_children(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"),
                                LeafNode("i", "Italic text"),
                                LeafNode(None, "Normal text")])
        node2 = ParentNode("p", None)
        node3 = ParentNode("p", [LeafNode("b", "Bold text"),
                                LeafNode("i", "Italic text"),
                                ParentNode("p", [LeafNode(None, "Normal text")])])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b><i>Italic text</i>Normal text</p>")
        self.assertEqual(node2.children, None)
        with self.assertRaises(ValueError):
            node2.to_html()
        self.assertEqual(node3.to_html(), "<p><b>Bold text</b><i>Italic text</i><p>Normal text</p></p>")

if __name__ == "__main__":
    unittest.main()
