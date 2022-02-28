import re
import statistics
from collections import defaultdict


def input_file(filename: str) -> str:
    text = open(filename, "r").read()
    return text


def get_words(text: str) -> list[str]:
    words = re.split(r"(?:(?:[^a-zA-Z]+')|(?:'[^a-zA-Z]+))|(?:[^a-zA-Z']+)", text)
    words_tmp = []
    for word in words:
        if len(word) > 0:
            words_tmp.append(word)
    words = words_tmp
    return words


def get_sentences_words(text: str) -> tuple[float, float]:
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    word_length: list[int] = []
    for sentence in sentences:
        if len(sentence) > 0:
            word_length.append(len(get_words(sentence)))
    average_amount = statistics.fmean(word_length)
    median_amount = statistics.median(word_length)
    return average_amount, median_amount


def get_words_count(words: list[str]) -> dict[str, int]:
    words_dict: dict[str, int] = defaultdict(int)
    for word in words:
        words_dict[word] += 1
    return words_dict


def get_ngrams(words_dict: dict[str, int], n: int) -> dict[str, int]:
    ngrams: dict[str, int] = defaultdict(int)
    for key, item in words_dict.items():
        for window in range(0, len(key) - n + 1):
            ngrams[key[window: window + n]] += item
    return ngrams


def input_data() -> tuple[int, int]:
    n: int = input("Input N: ")
    if n.isdigit():
        n = int(n)
    else:
        n = 4
    k: int = input("Input K: ")
    if k.isdigit():
        k = int(k)
    else:
        k = 10
    return n, k


def output_data(words_dict: dict[str, int], average_amount: float, median_amount: float,
                sorted_ngrams: list[str], k: int):
    print("Words dictionary:")
    for word, amount in words_dict.items():
        print(f"{word} = {amount}")
    print(f"Average amount of words in sentences: {average_amount}")
    print(f"Median amount of words in sentences: {median_amount}")
    print("Top k  ngrams:")
    for index in range(len(sorted_ngrams) - 1, len(sorted_ngrams) - k - 1, -1):
        print(f" {sorted_ngrams[index][0]} = {sorted_ngrams[index][1]}")
        if index == 0:
            break


def main():
    text = input_file("input.txt")
    n, k = input_data()
    print("Text:\n", text, sep='')
    text = text.lower()
    words = get_words(text)
    words_dict = get_words_count(words)
    average_amount, median_amount = get_sentences_words(text)
    ngrams = get_ngrams(words_dict, n)
    sorted_ngrams = sorted(ngrams.items(), key=lambda x: x[1])
    output_data(words_dict, average_amount, median_amount, sorted_ngrams, k)


if __name__ == "__main__":
    main()
