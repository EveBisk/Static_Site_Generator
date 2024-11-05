import unittest

from textnode import TextNode, TextType, TextTypeEnumException


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node", TextType.bold)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node", TextType.normal)
        self.assertNotEqual(node, node2)

    def test_repr_prints_expected_string(self):
        node = TextNode("Text", TextType.bold, "url").__repr__()
        expected_str = "TextNode(TEXT, BOLD, URL)"
        self.assertEqual(node, expected_str)

    def test_repr_prints_expected_string_with_url_None(self):
        node = TextNode("Text", TextType.bold).__repr__()
        expected_str = "TextNode(TEXT, BOLD, None)"
        self.assertEqual(node, expected_str)

    def test_text_type_not_in_Enum_raises_exception(self):
        with self.assertRaises(TextTypeEnumException):
            TextNode("Text", "other")


if __name__ == "__main__":
    unittest.main()
