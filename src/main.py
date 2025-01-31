from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utility import *
from markdown import *
from generatepage import generate_pages_recursive, generate_page
import os
import shutil

dir_path_static = "./static/"
dir_path_public = "./public/"
dir_path_content = "./content/"
template_path = "./template.html"
        
def main():
    #text = "![LOTR image artistmonkeys](/images/rivendell.png)"    

    generate_public_files()    
    
    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_public)

def generate_public_files():

    if not os.path.exists(dir_path_static):
        raise Exception("File Path: static not found")
    
    if not os.path.exists(dir_path_public):
        os.mkdir(dir_path_public)
    else:
        shutil.rmtree(dir_path_public)
        os.mkdir(dir_path_public)    

    copy_files(dir_path_static, dir_path_public)


def copy_files(src, dest):
    contents = os.listdir(src)

    for content in contents:
        new_path = os.path.join(src, content)        
        if os.path.isfile(new_path):
            print(f"Copying {content} to {dest}")
            shutil.copy(new_path, dest)
        else:
            new_dest = os.path.join(dest, f"{content}/")
            if not os.path.exists(new_dest):
                os.mkdir(new_dest)
            copy_files(new_path, new_dest) 
        

main()