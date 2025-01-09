from unittest import TestCase
from block_manipulation import BlockManipulation, BlockType
from leafnode import LeafNode
from parentnode import ParentNode

class TestBlockManipulationMarkDownToBlocks(TestCase):
    def test_single_block_unchanged(self):
        text = "This is one block"

        expected_result = [text]
        actual_result = BlockManipulation.markdown_to_blocks(text)

        self.assertEqual(expected_result, actual_result)

    def test_removes_new_lines(self):
        text = """
        This is one block
        
        
        """

        expected_result = ["This is one block"]
        actual_result = BlockManipulation.markdown_to_blocks(text)

        self.assertEqual(expected_result, actual_result)

    def test_removes_spaces(self):
        text = """  This is one block  """

        expected_result = ["This is one block"]
        actual_result = BlockManipulation.markdown_to_blocks(text)

        self.assertEqual(expected_result, actual_result)

    def test_ignores_single_lines(self):
        text = """
This is one block
With 2 lines
        """

        expected_result = ["This is one block\nWith 2 lines"]
        actual_result = BlockManipulation.markdown_to_blocks(text)

        self.assertEqual(expected_result, actual_result)

    def test_splits_two_blocks(self):
        text = """
This is one block

This is a second block.
        """

        expected_result = ["This is one block", "This is a second block."]
        actual_result = BlockManipulation.markdown_to_blocks(text)

        self.assertEqual(expected_result, actual_result)


class TestBlockManipulationValidOrderedList(TestCase):
    def test_valid_ordered_list(self):
        block = f"""1. Item One
2. Item Two"""

        is_ordered_list = BlockManipulation.is_valid_ordered_list(block)
        self.assertEqual(True, is_ordered_list)

    def test_invalid_ordered_list(self):
        block = f"""1. Item One
1. Item Two"""

        is_ordered_list = BlockManipulation.is_valid_ordered_list(block)
        self.assertEqual(False, is_ordered_list)


class TestBlockManipulation_BlockToBlockType(TestCase):
    def test_heading(self):
        block = "# Heading"
        block_type = BlockManipulation.block_to_block_type(block)

        self.assertEqual(BlockType.heading,block_type)

    def test_valid_code(self):
        block = "```\nCode\n```"
        block_type = BlockManipulation.block_to_block_type(block)

        self.assertEqual(BlockType.code, block_type)

    def test_invalid_code(self):
        block = "```\nCode\n`"
        block_type = BlockManipulation.block_to_block_type(block)

        self.assertEqual(BlockType.paragraph, block_type)

    def test_valid_quote(self):
        block = "> Line one\n> Line two"
        block_type = BlockManipulation.block_to_block_type(block)

        self.assertEqual(BlockType.quote, block_type)

    def test_invalid_quote(self):
        block = "> Line one\n Line two"
        block_type = BlockManipulation.block_to_block_type(block)

        self.assertEqual(BlockType.paragraph, block_type)

    def test_valid_unordered_list_ast(self):
        block = "* Line one\n* Line two"
        block_type = BlockManipulation.block_to_block_type(block)

        self.assertEqual(BlockType.unordered_list, block_type)

    def test_invalid_unordered_list_ast(self):
        block = "* Line one\n Line two"
        block_type = BlockManipulation.block_to_block_type(block)

        self.assertEqual(BlockType.paragraph, block_type)

    def test_valid_unordered_list_pavla(self):
        block = "- Line one\n- Line two"
        block_type = BlockManipulation.block_to_block_type(block)

        self.assertEqual(BlockType.unordered_list, block_type)

    def test_invalid_unordered_list_pavla(self):
        block = "- Line one\nLine two"
        block_type = BlockManipulation.block_to_block_type(block)

        self.assertEqual(BlockType.paragraph, block_type)

    def test_valid_ordered_list(self):
        block = "1. Line one\n2. Line two"
        block_type = BlockManipulation.block_to_block_type(block)

        self.assertEqual(BlockType.ordered_list, block_type)

    def test_invalid_ordered_list(self):
        block = "1. Line one\n Line two"
        block_type = BlockManipulation.block_to_block_type(block)

        self.assertEqual(BlockType.paragraph, block_type)

class TestBlockManipulation_block_to_children(TestCase):
    def test_paragraph(self):
        block = "This is a test paragraph."
        result = BlockManipulation.block_to_children(block)

        self.assertEqual(result.tag, "p")
        self.assertEqual(result.children[0].value, "This is a test paragraph.")

    def test_heading(self):
        block = "### This is a heading"
        result = BlockManipulation.block_to_children(block)

        self.assertEqual(result.tag, "h3")
        self.assertEqual(result.children[0].value, "This is a heading")

    def test_quote(self):
        block = "> This is a quote."
        result = BlockManipulation.block_to_children(block)

        self.assertEqual(result.tag, "blockquote")
        self.assertEqual(result.children[0].value, "This is a quote.")

    def test_code(self):
        block = "```code block```"
        result = BlockManipulation.block_to_children(block)

        self.assertEqual(result.tag, "pre")
        self.assertEqual(result.children[0].tag, "code")

    def test_unordered_list(self):
        block = "* Item 1\n* Item 2"
        result = BlockManipulation.block_to_children(block)

        self.assertEqual(result.tag, "ul")
        self.assertEqual(len(result.children), 2)

    def test_ordered_list(self):
        block = "1. Item 1\n2. Item 2"
        result = BlockManipulation.block_to_children(block)

        self.assertEqual(result.tag, "ol")
        self.assertEqual(len(result.children), 2)


class TestBlockManipulation_MarkdownToHtmlNode(TestCase):
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = BlockManipulation.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = BlockManipulation.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

    """

        node = BlockManipulation.markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>"

        self.assertEqual(
            html,
            expected_html,
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
    """

        node = BlockManipulation.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = BlockManipulation.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )
