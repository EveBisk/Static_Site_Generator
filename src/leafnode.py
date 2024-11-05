from htmlnode import HtmlNode


class LeafNode(HtmlNode):
    def __init__(self, value, tag=None, props=None):
        self.tag = tag
        self.value = value
        self.props = props

        super().__init__(
            tag=self.tag,
            value=self.value,
            children=None,
            props=self.props,
        )

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode Object must have value")

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
