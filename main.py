import re


def input_file(filename: str) -> str:
    text = open(filename, "r").read()
    return text


def text_analytics(text: str):
    text.lower()
    pass


def main():
    n = input("Input N: ")
    if n == "":
        n = 4
    k = input("Input K: ")
    if k == "":
        k = 10
    text = input_file("input.txt")
    print("Text:\n", text, sep = '')


if __name__ == "__main__":
    main()
