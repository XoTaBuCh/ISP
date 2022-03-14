import functions


def main():
    text = functions.input_file("input.txt")
    n, k = functions.input_data()
    print("Text:\n", text, sep='')

    text = text.lower()
    words = functions.get_words(text)
    words_dict = functions.get_words_count(words)
    average_amount, median_amount = functions.get_sentences_words(text)
    ngrams = functions.get_ngrams(words_dict, n)
    sorted_ngrams = sorted(ngrams.items(), key=lambda x: x[1])

    functions.output_data(words_dict, average_amount, median_amount, sorted_ngrams, k)


if __name__ == "__main__":
    main()
