import re
from htmlnode import *
from utility import text_to_textnodes, text_node_to_html_node

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)

    filtered_blocks = list(filter(None, filtered_blocks))
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")
    
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return "heading"
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return "code"
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return "paragraph"
        return "quote"
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return "paragraph"
        return "unordered_list"
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return "paragraph"
        return "unordered_list"
    if block.startswith("1. "):
        for line in lines:
            if len(re.findall(r"(^[0-9]{1,3}\.) .*", line)) == 0:
                return "paragraph"
        return "ordered_list"
        
    return "paragraph"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    all_blocks = []

    for block in blocks:
        # code/quote/unordered_list/ordered_list/paragraph/heading
        block_type = block_to_block_type(block)

        match block_type:
            case "heading":                        
                count = 0
                for letter in block:
                    if letter == "#":
                        count += 1
                    else:
                        break
                text = block.lstrip("#").strip()
                children = text_to_children(text)
                all_blocks.append(ParentNode(f"h{count}", children))

            case "paragraph":
                lines = block.split("\n")
                paragraph = " ".join(lines)
                children = text_to_children(paragraph)
                all_blocks.append(ParentNode("p", children))

            case "quote":
                text = block.lstrip(">").strip()
                children = text_to_children(text)
                all_blocks.append(ParentNode("blockquote", children))

            case "code":
                text = block.lstrip("`")
                text = text.rstrip("`")
                all_blocks.append(ParentNode("pre", [ParentNode("code", [LeafNode(None, text)])]))
            
            case "ordered_list":
                lines = block.split("\n")
                list_children = []
                for line in lines:                    
                    text = line.lstrip("0123456789.")
                    text = text.strip()
                    children = text_to_children(text)                    
                    list_children.append(ParentNode("li", children))
                all_blocks.append(ParentNode("ol", list_children))
                    
            case "unordered_list":
                lines = block.split("\n")
                list_children = []
                for line in lines:
                    text = line.lstrip("*-")
                    text = text.strip()
                    children = text_to_children(text)
                    list_children.append(ParentNode("li", children))
                all_blocks.append(ParentNode("ul", list_children))
                    
    return ParentNode("div", all_blocks)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block.lstrip("#").strip()
        
    raise Exception("Markdown Error: No h1 header found in document")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes
