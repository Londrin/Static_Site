import re

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
    
    if block.startswith(("#", "##", "###", "####", "#####", "######")):
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