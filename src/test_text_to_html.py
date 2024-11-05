from unittest import TestCase
from text_to_html import TextToHTMLConverter
from textnode import TextNode, TextType
from leafnode import LeafNode


class TextToHTMLConverterTest(TestCase):
    default_text = "This is a text node"

    def test_bold_converts_successfully(self):
        node = TextNode(self.default_text, TextType.bold)
        expected_leaf_node = LeafNode(self.default_text, tag="b")
        actual_leaf_node = TextToHTMLConverter.text_node_to_html_node(node)

        self.assertEqual(expected_leaf_node, actual_leaf_node)

    def test_normal_converts_successfully(self):
        node = TextNode(self.default_text, TextType.normal)
        expected_leaf_node = LeafNode(self.default_text)
        actual_leaf_node = TextToHTMLConverter.text_node_to_html_node(node)

        self.assertEqual(expected_leaf_node, actual_leaf_node)

    def test_italic_converts_successfully(self):
        node = TextNode(self.default_text, TextType.italic)
        expected_leaf_node = LeafNode(self.default_text, tag="i")
        actual_leaf_node = TextToHTMLConverter.text_node_to_html_node(node)

        self.assertEqual(expected_leaf_node, actual_leaf_node)

    def test_code_converts_successfully(self):
        node = TextNode(self.default_text, TextType.code)
        expected_leaf_node = LeafNode(self.default_text, tag="code")
        actual_leaf_node = TextToHTMLConverter.text_node_to_html_node(node)

        self.assertEqual(expected_leaf_node, actual_leaf_node)

    def test_links_converts_successfully(self):
        node = TextNode(self.default_text, TextType.links, url="my_url")
        expected_leaf_node = LeafNode(self.default_text, tag="a", props={"href": "my_url"})
        actual_leaf_node = TextToHTMLConverter.text_node_to_html_node(node)

        self.assertEqual(expected_leaf_node, actual_leaf_node)

    def test_images_converts_successfully(self):
        node = TextNode(self.default_text, TextType.images, url="my_img")
        expected_leaf_node = LeafNode("", tag="img", props={"src": "my_url", "alt": self.default_text})
        actual_leaf_node = TextToHTMLConverter.text_node_to_html_node(node)

        self.assertEqual(expected_leaf_node, actual_leaf_node)
