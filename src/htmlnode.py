class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        string_attributes = ""
        if self.props is not None: 
            for attribute in self.props:
                string_attributes += (f' {attribute}="{self.props[attribute]}"')
        return string_attributes

    def __repr__(self):
        string_list = []
        if self.tag is not None:
            string_list.append(f"tag: {self.tag}")
        if self.value is not None:
            string_list.append(f"value: {self.value}")
        if self.children is not None:
            string_list.append(self.get_children_string())
        if self.props is not None:
            string_list.append(f"props: {self.props}")
        rep_string = "\n".join(string_list)
        return f"HTML Node: {{\n{rep_string}\n}}"
        
    
    def get_children_string(self):
        if self.children is not None:
            children_strings = map(lambda x: f"--> |{x}|", self.children)
            full_string = ",\n".join(children_strings)
            return f"children: [\n{full_string}\n]"
        else:
            return ""

class LeafNode(HTMLNode):
    def __init__(self, tag=None, props=None, *, value):
        super().__init__(tag=tag, props=props, value=value)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        open_tag = f"<{self.tag}{self.props_to_html()}>"
        close_tag = f"</{self.tag}>"
        return f"{open_tag}{self.value}{close_tag}"

class ParentNode(HTMLNode):
    def __init__(self, props=None, *, tag, children):
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag.")
        if self.children is None or len(self.children) < 1:
            raise ValueError("All parent nodes must have at least one child node.")
        open_tag = f"<{self.tag}{self.props_to_html()}>"
        close_tag = f"</{self.tag}>"
        children_string_list = list(map(lambda x : x.to_html(), self.children))
        full_children_string = "".join(children_string_list)
        return f"{open_tag}{full_children_string}{close_tag}"