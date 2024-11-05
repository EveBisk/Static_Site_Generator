import unittest

from htmlnode import HtmlNode


class TestHtmlNode(unittest.TestCase):
    def test_raises_not_implemented_exception(self):
        with self.assertRaises(NotImplementedError):
            HtmlNode('a', 'a', None, None).to_html()

    def props_to_html_converts_one_row(self):
        props = {'a': 'aa'}
        expected_output = 'a="aa"'
        actual = HtmlNode(None, 'a', None, props)

        self.assertEqual(expected_output, actual)

    def props_to_html_converts_two_rows(self):
        props = {'a': 'aa', 'b': 'bb'}
        expected_output = 'a="aa" b="bb'
        actual = HtmlNode(None, 'a', None, props)

        self.assertEqual(expected_output, actual)

    # Copied from site

    def test_to_html_props(self):
        node = HtmlNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HtmlNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )


if __name__ == "__main__":
    unittest.main()
