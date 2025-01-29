import unittest
from markdown import block_to_block_type, markdown_to_blocks

class TestMardown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = "# This is a heading\n\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item\n\n\n\n\n\n\n\n\n"
        result = markdown_to_blocks(text)
        self.assertListEqual(result, ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item'])

        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_type_heading(self):
        md = "# Heading"
        md1 = "## Heading"
        md2 = "### Heading"
        md3 = "#### Heading"
        md4 = "##### Heading"
        md5 = "###### Heading"
        self.assertEqual(block_to_block_type(md), "heading")
        self.assertEqual(block_to_block_type(md1), "heading")
        self.assertEqual(block_to_block_type(md2), "heading")
        self.assertEqual(block_to_block_type(md3), "heading")
        self.assertEqual(block_to_block_type(md4), "heading")
        self.assertEqual(block_to_block_type(md5), "heading")
    
    def test_block_type_code(self):        
        md = """```\ncode\n```"""        
        self.assertEqual(block_to_block_type(md), "code")

    def test_block_type_quote(self):
        md = "> quote"
        md1 = "> quote\n> new quote\n> third quote"
        self.assertEqual(block_to_block_type(md), "quote")
        self.assertEqual(block_to_block_type(md1), "quote")

    def test_block_type_unordered_list(self):
        md = "* object"
        md1 = "- different object"
        self.assertEqual(block_to_block_type(md), "unordered_list")
        self.assertEqual(block_to_block_type(md1), "unordered_list")

    def test_block_type_ordered_list(self):
        md = "1. list"
        md1 = "1. list\n2. new\n3. newer"
        self.assertEqual(block_to_block_type(md), "ordered_list")
        self.assertEqual(block_to_block_type(md1), "ordered_list")

    def test_block_type_paragraph(self):
        md = "We will go out on our own"
        self.assertEqual(block_to_block_type(md), "paragraph")

if __name__ == "__main__":
    unittest.main()