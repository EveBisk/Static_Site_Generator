from unittest import TestCase
from text_mainipulation import TextManipulation
from textnode import TextType, TextNode


class TestTextManipulationSplitNodeDelimiter(TestCase):
    def test_if_not_text_returns_old(self):
        old_nodes = [TextNode("Hello", TextType.code)]
        result = TextManipulation.split_nodes_delimiter(old_nodes, "*", TextType.code)

        self.assertEqual(old_nodes, result)

    def split_success(self):
        node = [TextNode("This is text with a `code block` word", TextType.text)]
        new_nodes = TextManipulation.split_nodes_delimiter([node], "`", TextType.code)

        expected_nodes = [
            TextNode("This is text with a ", TextType.text),
            TextNode("code block", TextType.code),
            TextNode(" word", TextType.text),
        ]

        self.assertEqual(new_nodes, expected_nodes)


class TestTextManipulationDelimiterToTextNde(TestCase):
    test_string = "Hello! This is test!"

    def test_bold_text_node(self):
        result = TextManipulation.delimiter_to_text_node(
            self.test_string,
            "**"
        )
        self.assertEqual(
            result,
            TextNode(text=self.test_string, text_type=TextType.bold),
        )

    def test_italic_text_node(self):
        result = TextManipulation.delimiter_to_text_node(
            self.test_string,
            "*"
        )
        self.assertEqual(
            result,
            TextNode(text=self.test_string, text_type=TextType.italic),
        )

    def test_code_text_node(self):
        result = TextManipulation.delimiter_to_text_node(
            self.test_string,
            "`"
        )
        self.assertEqual(
            result,
            TextNode(text=self.test_string, text_type=TextType.code),
        )

    def test_normal_text_node(self):
        result = TextManipulation.delimiter_to_text_node(
            self.test_string,
            ""
        )
        self.assertEqual(
            result,
            TextNode(text=self.test_string, text_type=TextType.text),
        )


class TestTextManipulationExtractMarkdownImages(TestCase):
    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and text"
        result = TextManipulation.extract_markdown_images(
            text
        )
        self.assertEqual(
            result,
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif")],
        )

    def test_no_image(self):
        result = TextManipulation.extract_markdown_images(
            "No images here",
        )
        self.assertEqual(
            result,
            []
        )

    def test_ignores_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and text"
        result = TextManipulation.extract_markdown_images(
            text
        )
        self.assertEqual(
            result,
            [],
        )


class TestTextManipulationExtractMarkdownLinks(TestCase):
    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and text"
        result = TextManipulation.extract_markdown_links(
            text
        )
        self.assertEqual(
            result,
            [("to boot dev", "https://www.boot.dev")],
        )

    def test_no_image(self):
        result = TextManipulation.extract_markdown_images(
            "No links here",
        )
        self.assertEqual(
            result,
            []
        )

    def test_ignores_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and text"
        result = TextManipulation.extract_markdown_links(
            text
        )
        self.assertEqual(
            result,
            [],
        )


class TestTextManipulationSplitNodesImage(TestCase):
    def test_ignores_non_text_types(self):
        nodes = [TextNode(text="bold string", text_type=TextType.bold)]
        result = TextManipulation.split_nodes_image(
            nodes
        )
        self.assertEqual(
            result,
            nodes,
        )

    def test_splits_one_image_correctly(self):
        url = "https://i.imgur.com/aKaOqIh.gif"
        alt = "rick roll"

        text = f"This is text with a ![{alt}]({url}) and text"
        nodes = [TextNode(text=text, text_type=TextType.text)]

        expected_result = [
            TextNode(text="This is text with a ", text_type=TextType.text),
            TextNode(text=alt, text_type=TextType.images, url=url),
            TextNode(text=" and text", text_type=TextType.text),
        ]
        actual_result = TextManipulation.split_nodes_image(
            nodes
        )

        self.assertEqual(expected_result, actual_result)

    def test_splits_two_images_correctly(self):
        url1 = "https://i.imgur.com/aKaOqIh.gif"
        alt1 = "rick roll"

        url2 = "https://www.youtube.com/@bootdotdev"
        alt2 = "to youtube"

        text = f"This is text with a ![{alt1}]({url1}) and ![{alt2}]({url2})"
        nodes = [TextNode(text=text, text_type=TextType.text)]

        expected_result = [
            TextNode(text="This is text with a ", text_type=TextType.text),
            TextNode(text=alt1, text_type=TextType.images, url=url1),
            TextNode(text=" and ", text_type=TextType.text),
            TextNode(text=alt2, text_type=TextType.images, url=url2),
        ]
        actual_result = TextManipulation.split_nodes_image(
            nodes
        )

        self.assertEqual(expected_result, actual_result)

    def test_splits_two_images_correctly_extra_text(self):
        url1 = "https://i.imgur.com/aKaOqIh.gif"
        alt1 = "rick roll"

        url2 = "https://www.youtube.com/@bootdotdev"
        alt2 = "to youtube"

        text = f"This is text with a ![{alt1}]({url1}) and ![{alt2}]({url2}) and extra text"
        nodes = [TextNode(text=text, text_type=TextType.text)]

        expected_result = [
            TextNode(text="This is text with a ", text_type=TextType.text),
            TextNode(text=alt1, text_type=TextType.images, url=url1),
            TextNode(text=" and ", text_type=TextType.text),
            TextNode(text=alt2, text_type=TextType.images, url=url2),
            TextNode(text=" and extra text", text_type=TextType.text)
        ]
        actual_result = TextManipulation.split_nodes_image(
            nodes
        )

        self.assertEqual(expected_result, actual_result)


class TestTextManipulationSplitNodesLinks(TestCase):
    def test_ignores_non_text_types(self):
        nodes = [TextNode(text="bold string", text_type=TextType.bold)]
        result = TextManipulation.split_nodes_link(
            nodes
        )
        self.assertEqual(
            result,
            nodes,
        )

    def test_splits_one_link_correctly(self):
        url = "https://i.imgur.com/aKaOqIh.gif"
        alt = "rick roll"

        text = f"This is text with a [{alt}]({url}) and text"
        nodes = [TextNode(text=text, text_type=TextType.text)]

        expected_result = [
            TextNode(text="This is text with a ", text_type=TextType.text),
            TextNode(text=alt, text_type=TextType.links, url=url),
            TextNode(text=" and text", text_type=TextType.text),
        ]
        actual_result = TextManipulation.split_nodes_link(
            nodes
        )

        self.assertEqual(expected_result, actual_result)

    def test_splits_two_links_correctly(self):
        url1 = "https://i.imgur.com/aKaOqIh.gif"
        alt1 = "rick roll"

        url2 = "https://www.youtube.com/bootdotdev"
        alt2 = "to youtube"

        text = f"This is text with a [{alt1}]({url1}) and [{alt2}]({url2})"
        nodes = [TextNode(text=text, text_type=TextType.text)]

        expected_result = [
            TextNode(text="This is text with a ", text_type=TextType.text),
            TextNode(text=alt1, text_type=TextType.links, url=url1),
            TextNode(text=" and ", text_type=TextType.text),
            TextNode(text=alt2, text_type=TextType.links, url=url2)
        ]
        actual_result = TextManipulation.split_nodes_link(
            nodes
        )

        self.assertEqual(expected_result, actual_result)

    def test_splits_two_links_correctly_extra_text(self):
        url1 = "https://i.imgur.com/aKaOqIh.gif"
        alt1 = "rick roll"

        url2 = "https://www.youtube.com/bootdotdev"
        alt2 = "to youtube"

        text = f"This is text with a [{alt1}]({url1}) and [{alt2}]({url2}) and extra text"
        nodes = [TextNode(text=text, text_type=TextType.text)]

        expected_result = [
            TextNode(text="This is text with a ", text_type=TextType.text),
            TextNode(text=alt1, text_type=TextType.links, url=url1),
            TextNode(text=" and ", text_type=TextType.text),
            TextNode(text=alt2, text_type=TextType.links, url=url2),
            TextNode(text=" and extra text", text_type=TextType.text)
        ]
        actual_result = TextManipulation.split_nodes_link(
            nodes
        )

        self.assertEqual(expected_result, actual_result)

class TestTextManipulationTextTotextNode(TestCase):
    def test_plain_text(self):
        text = "Some plain text"

        expected_result =[TextNode(text=text, text_type=TextType.text)]
        actual_result = TextManipulation.text_to_textnode(text)

        self.assertEqual(expected_result,actual_result)

    def test_splits_all_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        expected_result = [
            TextNode("This is ", TextType.text),
            TextNode("text", TextType.bold),
            TextNode(" with an ", TextType.text),
            TextNode("italic", TextType.italic),
            TextNode(" word and a ", TextType.text),
            TextNode("code block", TextType.code),
            TextNode(" and an ", TextType.text),
            TextNode("obi wan image", TextType.images, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.text),
            TextNode("link", TextType.links, "https://boot.dev"),
        ]

        actual_result = TextManipulation.text_to_textnode(text)

        self.assertEqual(expected_result, actual_result)
