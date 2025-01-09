from textnode import TextNode, TextType
import os
import shutil

from page_generation import GeneratePage

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def copy_directory(source, destination):
    if not os.path.exists(source):
        print(f"Source directory '{source}' does not exist.")
        raise FileNotFoundError(f"Source directory '{source}' does not exist.")

    if os.path.exists(destination):
        print(f"Deleting contents of destination directory '{destination}'...")
        shutil.rmtree(destination)

    print(f"Creating destination directory '{destination}'...")
    os.makedirs(destination)

    for root, dirs, files in os.walk(source):
        relative_path = os.path.relpath(root, source)
        dest_dir = os.path.join(destination, relative_path)

        if not os.path.exists(dest_dir):
            print(f"Creating directory '{dest_dir}'...")
            os.makedirs(dest_dir, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, file)
            print(f"Copying file '{src_file}' to '{dest_file}'...")
            shutil.copy2(src_file, dest_file)

    print(f"All contents copied from '{source}' to '{destination}' successfully.")


def __main__():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")

    print("Copying static files to public directory...")
    copy_directory("static", "public")

    print("Generating pages...")
    GeneratePage.generate_pages_recursive(dir_path_content, template_path, dir_path_public)


__main__()
