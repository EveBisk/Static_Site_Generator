from unittest import TestCase
from parentnode import ParentNode
from leafnode import LeafNode


class ParentNodeTest(TestCase):
    simple_child = LeafNode("Simple raw text")

    def test_none_children_raises_value_error(self):
        parent_node = ParentNode(None, tag='a')

        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_none_tag_raises_value_error(self):
        parent_node = ParentNode([self.simple_child])

        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_single_child_returns_correct_sting(self):
        parent_node = ParentNode([self.simple_child], tag='p')
        expected_str = f"<p>{self.simple_child.to_html()}</p>"

        self.assertEqual(expected_str, parent_node.to_html())

    def test_node_with_props_returns_correct_sting(self):
        parent_node = ParentNode([self.simple_child], tag='a', props={"href":"google.com"})
        expected_str = f'<a href="google.com">{self.simple_child.to_html()}</a>'

        self.assertEqual(expected_str, parent_node.to_html())

    def test_multiple_children_returns_correct_sting(self):
        parent_node = ParentNode(
            [
                LeafNode( "Bold text","b"),
                LeafNode("Normal text", None),
                LeafNode("italic text", "i"),
                LeafNode("Normal text", None),
            ],
            "p"
        )
        expected_str = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"

        self.assertEqual(expected_str, parent_node.to_html())

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("grandchild", "b")
        child_node = ParentNode([grandchild_node], "span")
        parent_node = ParentNode([child_node], "div")
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
