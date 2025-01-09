from leafnode import LeafNode
from textnode import TextType


class TextToHTMLConverter:
    @staticmethod
    def text_node_to_html_node(text_node):
        text_type = TextType[text_node.text_type]

        match text_type:
            case TextType.bold:
                return LeafNode(value=text_node.text, tag="b")
            case TextType.text:
                return LeafNode(value=text_node.text)
            case TextType.italic:
                return LeafNode(value=text_node.text, tag="i")
            case TextType.code:
                return LeafNode(value=text_node.text, tag="code")
            case TextType.links:
                return LeafNode(value=text_node.text, tag="a", props={"href": text_node.url})
            case TextType.images:
                return LeafNode(value="", tag="img", props={"src": text_node.url, "alt": text_node.text})
