import re
from enum import Enum

from leafnode import  LeafNode
from parentnode import ParentNode
from text_mainipulation import TextManipulation
from text_to_html import TextToHTMLConverter


class BlockType(Enum):
    heading = ("heading", None)
    paragraph = "paragraph"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"


class BlockManipulation:
    @staticmethod
    def markdown_to_blocks(markdown):
        blocks = markdown.split("\n\n")
        return [block.strip("\n").strip() for block in blocks if block.strip() != ""]

    @staticmethod
    def is_valid_ordered_list(block):
        lines = block.split("\n")

        for index, line in enumerate(lines, start=1):
            if not line.startswith(f"{index}. "):
                return False
        return True

    @staticmethod
    def block_to_block_type(block):

        if block.startswith("#"):
            return BlockType.heading

        if block.startswith("```") and block.endswith("```"):
            return BlockType.code

        if block.startswith(">"):
            lines = block.split("\n")
            if all(line.startswith(">") for line in lines):
                return BlockType.quote

        if block.startswith("* ") or block.startswith("- "):
            lines = block.split("\n")
            if all(line.startswith("* ") or line.startswith("- ") for line in lines):
                return BlockType.unordered_list

        if block.startswith("1. "):
            if BlockManipulation.is_valid_ordered_list(block):
                return BlockType.ordered_list

        return BlockType.paragraph

    @staticmethod
    def text_to_html_children(text):
        text_nodes = TextManipulation.text_to_textnode(text)
        children = []
        for text_node in text_nodes:
            html_node = TextToHTMLConverter.text_node_to_html_node(text_node)
            children.append(html_node)
        return children

    @staticmethod
    def block_to_children(block):
        block_type = BlockManipulation.block_to_block_type(block)

        match block_type:
            case BlockType.paragraph:
                lines = block.split("\n")
                paragraph = " ".join(lines)
                children = BlockManipulation.text_to_html_children(paragraph)
                return ParentNode(children=children, tag="p")

            case BlockType.heading:
                hash_count = block.count("#")
                text = block.lstrip("#").strip()
                children = BlockManipulation.text_to_html_children(text)

                return ParentNode(children=children, tag= f"h{hash_count}")

            case BlockType.quote:
                text = block.replace("> ", "").replace("\n", " ")
                children = BlockManipulation.text_to_html_children(text)
                return ParentNode(children=children, tag="blockquote")

            case BlockType.code:
                text = block.lstrip("```").rstrip("```").strip()
                children = BlockManipulation.text_to_html_children(text)
                child_node = [ParentNode(children, tag="code")]
                return ParentNode(children=child_node, tag="pre")

            case BlockType.unordered_list:
                lines = block.split("\n")

                list_children = []
                for line in lines:
                    text = line.lstrip("*").lstrip("-").strip()
                    text_children = BlockManipulation.text_to_html_children(text)
                    list_children.append(ParentNode(children=text_children, tag="li"))

                return ParentNode(children=list_children, tag="ul")

            case BlockType.ordered_list:
                lines = block.split("\n")
                cleaned_lines = [re.sub(r"^\d+\.\s*", "", line) for line in lines]

                list_children = []
                for line in cleaned_lines:
                    text = line.strip()
                    text_children = BlockManipulation.text_to_html_children(text)
                    list_children.append(ParentNode(children=text_children, tag="li"))

                return ParentNode(children=list_children, tag="ol")


    @staticmethod
    def markdown_to_html_node(markdown):
        blocks = BlockManipulation.markdown_to_blocks(markdown)
        children_nodes = []

        for block in blocks:
            node = BlockManipulation.block_to_children(block)
            children_nodes.append(node)

        parent_node = ParentNode(children=children_nodes, tag="div")
        return parent_node


