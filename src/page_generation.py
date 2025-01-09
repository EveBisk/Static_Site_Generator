import os
from block_manipulation import BlockManipulation


class GeneratePage:
    @staticmethod
    def extract_title(markdown):
        has_header = markdown.startswith("# ")

        if not has_header:
            raise ValueError("Header not found")

        return markdown.lstrip("#").strip()

    @staticmethod
    def generate(from_path, template_path, dest_path):
        print(f"Generating page from {from_path} to {dest_path} using {template_path}")

        if not os.path.exists(from_path):
            raise FileNotFoundError(f"Markdown file '{from_path}' does not exist.")
        with open(from_path, "r", encoding="utf-8") as f:
            markdown_content = f.read()

        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template file '{template_path}' does not exist.")
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        html_node = BlockManipulation.markdown_to_html_node(markdown_content)
        html_content = html_node.to_html()

        title = GeneratePage.extract_title(markdown_content)

        html_page = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(html_page)

        print(f"Page successfully generated at {dest_path}")

    @staticmethod
    def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

        if not os.path.exists(dir_path_content):
            raise FileNotFoundError(f"Path {dir_path_content} does not exist")

        for directory, _, filelist in os.walk(dir_path_content):
            print(f"Inspecting directory {directory}")

            for file in filelist:
                print(f"Inspecting file {file}")
                from_path = os.path.join(directory, file)
                dest_dir = directory.replace(dir_path_content, dest_dir_path)
                new_file = file.replace("md", "html")
                dest_path = os.path.join(dest_dir, new_file)

                GeneratePage.generate(from_path, template_path, dest_path)
