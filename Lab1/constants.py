N_CONST = 4
K_CONST = 10

WORD_REGEX = r"(?:(?:[^a-zA-Z]+')|(?:'[^a-zA-Z]+))|(?:[^a-zA-Z']+)"
SENTENCE_REGEX = r"(?<!\w\.\w.)(?<![a-z][a-z]\.)(?<=\.|\?|!)\s"
