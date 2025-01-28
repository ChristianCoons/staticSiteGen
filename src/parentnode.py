from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None or children is None:
            raise ValueError("Parent nodes must have tag and child")
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        
        htmltext = f"<{self.tag}{self.props_to_html()}>"

        for child in self.children:
            htmltext += child.to_html()

        htmltext += f"</{self.tag}>"

        return htmltext
        