from unittest import TestCase
from leafnode import LeafNode


class LeafNodeTest(TestCase):
    def test_no_value_raises_error(self):
        leaf_node = LeafNode(None, "a", {"a": "aa"})

        with self.assertRaises(ValueError):
            leaf_node.to_html()

    def test_no_tag_returns_raw_string(self):
        leaf_node = LeafNode("text", None, {"a": "aa"})

        self.assertEqual("text", leaf_node.to_html())

    def test_tag_is_returned_correctly(self):
        leaf_node = LeafNode("text", "b")
        expected_str = "<b>text</b>"

        self.assertEqual(expected_str, leaf_node.to_html())

    def test_props_populated(self):
        leaf_node = LeafNode("text", "a", {"href":"www.google.com"})
        expected_str = '<a href="www.google.com">text</a>'

        self.assertEqual(expected_str, leaf_node.to_html())