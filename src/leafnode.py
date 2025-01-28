from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("All leaf nodes must have a value.")
        super().__init__(tag=tag, value=value, children=[], props=props)
    

    def to_html(self):
        returnString = ""
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        elif self.tag is None:
            return self.value
        # Special case for self-closing tags like img
        elif self.tag == "img":
            return f"<{self.tag}{self.props_to_html()}>"
        else:
            returnString += f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
        return returnString