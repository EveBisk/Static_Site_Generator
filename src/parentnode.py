from htmlnode import HtmlNode


class ParentNode(HtmlNode):
    def __init__(self, children, tag=None, props=None):
        self.children = children
        self.tag = tag
        self.props = props

        super().__init__(tag=self.tag, value=None, children=self.children, props=self.props)

    def to_html(self):
        if self.children is None:
            raise ValueError("Children cannot be None")

        if self.tag is None:
            raise ValueError("Tag cannot be None")

        full_string = ""
        for child in self.children:
            full_string += child.to_html()

        return  f"<{self.tag}{self.props_to_html()}>{full_string}</{self.tag}>"
