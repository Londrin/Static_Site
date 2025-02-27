import unittest

from htmlnode import LeafNode
from textnode import TextType, TextNode
from utility import *

class TestTextConversion(unittest.TestCase):
    def test_type_conversion(self):
        normal = TextNode("This is normal", TextType.NORMAL)
        bold = TextNode("This is bold", TextType.BOLD)
        italic = TextNode("This is italic", TextType.ITALIC)
        code = TextNode("This is code", TextType.CODE)
        image = TextNode("This image is beautiful", TextType.IMAGE, "https://image.boot.dev")
        link = TextNode("Go here", TextType.LINK, "https://www.boot.dev")

        self.assertEqual(text_node_to_html_node(normal), LeafNode(None, normal.text))
        self.assertEqual(text_node_to_html_node(bold), LeafNode("b", bold.text))
        self.assertEqual(text_node_to_html_node(italic), LeafNode("i", italic.text))
        self.assertEqual(text_node_to_html_node(code), LeafNode("code", code.text))
        self.assertEqual(text_node_to_html_node(image), LeafNode("img", "", {"src": image.url, "alt": image.text}))
        self.assertEqual(text_node_to_html_node(link), LeafNode("a", link.text, {"href": link.url}))       

    def test_type_no_url(self):
        image = TextNode("This image is beautiful", TextType.IMAGE, None)
        link = TextNode("Go here", TextType.LINK, None)
        with self.assertRaises(Exception):
            text_node_to_html_node(image)
        with self.assertRaises(Exception):
            text_node_to_html_node(link)

    def test_split_nodes(self):
        node = TextNode("This is text with a 'code block' word", TextType.NORMAL)
        node1 = TextNode("This is text with a **bold** word", TextType.NORMAL)
        node2 = TextNode("This is text with a *italic* word", TextType.NORMAL)
        node_no_delimiter = TextNode("This is text with a *italic word", TextType.NORMAL)
        node_wrong_type = TextNode("This is text with a bold sentence", TextType.BOLD)
        self.assertEqual(split_nodes_delimiter([node], "'", TextType.CODE), 
                         [TextNode("This is text with a ", TextType.NORMAL),
                          TextNode("code block", TextType.CODE),
                          TextNode(" word", TextType.NORMAL)])
        with self.assertRaises(Exception):
            split_nodes_delimiter([node_no_delimiter], "*", TextType.ITALIC)

        self.assertEqual(split_nodes_delimiter([node1], "**", TextType.BOLD), 
                         [TextNode("This is text with a ", TextType.NORMAL),
                          TextNode("bold", TextType.BOLD),
                          TextNode(" word", TextType.NORMAL)])
        self.assertEqual(split_nodes_delimiter([node2], "*", TextType.ITALIC), 
                         [TextNode("This is text with a ", TextType.NORMAL),
                          TextNode("italic", TextType.ITALIC),
                          TextNode(" word", TextType.NORMAL)])
        self.assertEqual(split_nodes_delimiter([node_wrong_type], "**", TextType.BOLD), [TextNode("This is text with a bold sentence", TextType.BOLD)])

    def test_split_multiple(self):
        node = TextNode("This is text with a **bold** word but **with** two", TextType.NORMAL)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), 
                         [TextNode("This is text with a ", TextType.NORMAL),
                          TextNode("bold", TextType.BOLD),
                          TextNode(" word but ", TextType.NORMAL),
                          TextNode("with", TextType.BOLD),
                          TextNode(" two", TextType.NORMAL)])
        
    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_regex_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        output = extract_markdown_images(text)
        self.assertEqual(output, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
        text = """
                Here's a [link](http://example.com)
                And an ![image](img.jpg)
                And a ![multi word image](pic.png)
                And a [multi word link](http://test.com)
                """
        output = extract_markdown_images(text)
        self.assertEqual(output, [("image", "img.jpg"), ("multi word image", "pic.png")])
    
    def test_regex_links(self):        
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        output = extract_markdown_links(text)
        self.assertEqual(output, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
        text = """
                Here's a [link](http://example.com)
                And an ![image](img.jpg)
                And a ![multi word image](pic.png)
                And a [multi word link](http://test.com)
                """
        output = extract_markdown_links(text)
        self.assertEqual(output, 
                         [("link", "http://example.com"),
                          ("multi word link", "http://test.com")])
            
    def test_split_link(self):        
        node = TextNode(
            "Start [first](img1.jpg) middle [second](img2.jpg) end", 
            TextType.NORMAL)        
        self.assertListEqual(split_nodes_link([node]), [TextNode("Start ", TextType.NORMAL, None), TextNode("first", TextType.LINK, "img1.jpg"), TextNode(" middle ", TextType.NORMAL, None), TextNode("second", TextType.LINK, "img2.jpg"), TextNode(" end", TextType.NORMAL, None)])

    def test_split_image_multiple(self):
        node = TextNode(
            "Start with ![first](img1.jpg) middle ![second](img2.jpg) end",
            TextType.NORMAL)
        self.assertListEqual(split_nodes_image([node]), [TextNode("Start with ", TextType.NORMAL, None), TextNode("first", TextType.IMAGE, "img1.jpg"), TextNode(" middle ", TextType.NORMAL, None), TextNode("second", TextType.IMAGE, "img2.jpg"), TextNode(" end", TextType.NORMAL, None)])
    
    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG")], 
            new_nodes)
        
    def test_text_to_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertListEqual(result, [TextNode("This is ", TextType.NORMAL),
                                      TextNode("text", TextType.BOLD),
                                      TextNode(" with an ", TextType.NORMAL),
                                      TextNode("italic", TextType.ITALIC),
                                      TextNode(" word and a ", TextType.NORMAL),
                                      TextNode("code block", TextType.CODE),
                                      TextNode(" and an ", TextType.NORMAL),
                                      TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                                      TextNode(" and a ", TextType.NORMAL),
                                      TextNode("link", TextType.LINK, "https://boot.dev")])



if __name__ == "__main__":
    unittest.main()
