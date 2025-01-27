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
        if self.tag is None:
            return self.value
        else:
            returnString += f"<{self.tag}"

            if self.props is None:
                returnString += f">"
            else:
                returnString += f"{self.props_to_html()}>"
            
            returnString += f"{self.value}</{self.tag}>"

        return returnString