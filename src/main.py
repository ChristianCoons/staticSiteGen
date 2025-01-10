print("hello world")
from textnode import *



def main():
        
        textNode = TextNode("This is a text Node", TextType.BOLD, "https://boot.dev")
        print(textNode.__repr__())
main()