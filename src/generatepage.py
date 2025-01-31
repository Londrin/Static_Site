from markdown import markdown_to_html_node, extract_title
import os
import shutil

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown_content = read_file_contents(from_path)
    template_content = read_file_contents(template_path)

    title = extract_title(markdown_content)
    html_content = markdown_to_html_node(markdown_content).to_html()
    
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_content)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(f"{dest_path}index.html", "w") as file:
        file.write(template_content)
    return

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):    

    #template = read_file_contents(template_path)

    dir_contents = os.listdir(dir_path_content)

    for content in dir_contents:
        new_content = os.path.join(dir_path_content, content)
        if os.path.isfile(new_content):            
            generate_page(new_content, template_path, dest_dir_path)            
        else:
            new_dest_dir_path = os.path.join(dest_dir_path, f"{content}")
            if not os.path.exists(new_dest_dir_path):
                os.mkdir(new_dest_dir_path)
            generate_pages_recursive(new_content, template_path, f"{new_dest_dir_path}/")

    return

def read_file_contents(path):
    content = ""
    with open(path, "r") as file:
        content = file.read()
        file.close()
    return content