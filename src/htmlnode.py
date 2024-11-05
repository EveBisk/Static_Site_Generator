class HtmlNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.children = children
        self.value = value
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""

        rows = [f' {key}="{value}"' for key, value in self.props.items()]
        return "".join(rows)

    def __eq__(self, other):
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == self.props
        )

    def __repr__(self):
        printable = f"""
HtmlNode:\ntag: {self.tag}\nvalue:{self.value}\n
children:{self.children}\nprops:{self.props}
"""
        return printable
