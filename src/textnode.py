from enum import Enum


class TextType(Enum):
    bold = "bold"
    italic = "italic"
    code = "code"
    links = "links"
    images = "images"
    text = "text"


class TextTypeEnumException(Exception):
    pass


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text: str = text
        if not isinstance(text_type, TextType):
            raise TextTypeEnumException("Text type not of TextType enum")
        self.text_type: str = text_type.value
        self.url: str | None = url

    def __eq__(self, other):
        return self.text_type == other.text_type and self.text == other.text and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text.upper()}, {self.text_type.upper()}, {(self.url.upper() if self.url is not None else None)})"
