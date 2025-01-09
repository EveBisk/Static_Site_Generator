from textnode import TextType, TextNode
import re

class TextManipulation:
    @staticmethod
    def split_nodes_delimiter(old_nodes, delimiter, text_type):
        new_nodes = []
        for old_node in old_nodes:
            if old_node.text_type != TextType.text.value:
                new_nodes.append(old_node)
                continue

            split_nodes = []
            sections = old_node.text.split(delimiter)
            if len(sections) % 2 == 0:
                raise ValueError("Invalid markdown, formatted section not closed")
            for i in range(len(sections)):
                if sections[i] == "":
                    continue
                if i % 2 == 0:
                    split_nodes.append(TextNode(sections[i], TextType.text))
                else:
                    split_nodes.append(TextNode(sections[i], text_type))
            new_nodes.extend(split_nodes)
        return new_nodes

    @staticmethod
    def delimiter_to_text_node(string, delimiter):
        match delimiter:
            case "**":
                return TextNode(text=string, text_type=TextType.bold)
            case "*":
                return TextNode(text=string, text_type=TextType.italic)
            case "`":
                return TextNode(text=string, text_type=TextType.code)
            case "":
                return TextNode(text=string, text_type=TextType.text)

    @staticmethod
    def extract_markdown_images(text):
        matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
        return matches

    @staticmethod
    def extract_markdown_links(text):
        matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
        return matches

    @staticmethod
    def split_nodes_image(old_nodes):
        new_nodes = []

        for old_node in old_nodes:
            if old_node.text_type != TextType.text.value:
                new_nodes.append(old_node)
            else:
                original_text = old_node.text

                image_matches = TextManipulation.extract_markdown_images(original_text)
                if image_matches:
                    text = original_text
                    len_matches = len(image_matches)
                    for i in range(len_matches):
                        alt, link = image_matches[i]
                        sections = text.split(f"![{alt}]({link})", 1)
                        new_nodes.append(TextNode(text=sections[0], text_type=TextType.text))
                        new_nodes.append(TextNode(text=alt, text_type=TextType.images, url=link))

                        if i == len_matches-1 and sections[1] != '':
                            new_nodes.append(TextNode(text=sections[1], text_type=TextType.text))
                        else:
                            text = sections[1]

                else:
                    new_nodes.append(old_node)

        return new_nodes

    @staticmethod
    def split_nodes_link(old_nodes):
        new_nodes = []

        for old_node in old_nodes:
            if old_node.text_type != TextType.text.value:
                new_nodes.append(old_node)

            else:
                original_text = old_node.text

                link_matches = TextManipulation.extract_markdown_links(original_text)

                if link_matches:
                    text = original_text

                    len_matches = len(link_matches)
                    for i in range(len_matches):
                        alt, link = link_matches[i]
                        sections = text.split(f"[{alt}]({link})", 1)

                        new_nodes.append(TextNode(text=sections[0], text_type=TextType.text))
                        new_nodes.append(TextNode(text=alt, text_type=TextType.links, url=link))

                        if i == len_matches-1 and sections[1] != '':
                            new_nodes.append(TextNode(text=sections[1], text_type=TextType.text))
                        else:
                            text = sections[1]
                else:
                    new_nodes.append(old_node)

        return new_nodes

    @staticmethod
    def text_to_textnode(text):
        initial_node = [TextNode(text=text, text_type=TextType.text)]

        bold_nodes = TextManipulation.split_nodes_delimiter(initial_node, '**', TextType.bold)
        italian_nodes = TextManipulation.split_nodes_delimiter(bold_nodes, "*", TextType.italic)
        code_nodes = TextManipulation.split_nodes_delimiter(italian_nodes, "`", TextType.code)

        image_nodes = TextManipulation.split_nodes_image(code_nodes)
        link_nodes = TextManipulation.split_nodes_link(image_nodes)

        return link_nodes
