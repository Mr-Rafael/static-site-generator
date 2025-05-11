from textnode import TextNode, TextType

def main():
    example = TextNode("1", TextType.LINK, "3")
    print(f"first node: {example}")
    without_url = TextNode("1", TextType.NORMAL)
    print(f"scond node: {without_url}")

main()