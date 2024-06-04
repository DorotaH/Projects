import random


def horner(word, p):
    sum = 0
    for letter in word:
        sum = (sum * 128 + ord(letter)) % p
    return sum


def naive_check(word1, word2):
    return word1 == word2


# O(n + m)
def rabinkarp(pattern, sentence):
    splitted = sentence.split("\n")
    p = 89
    changed_list = []
    indexes = []
    word_indexes = []
    word_counter = 0
    new_song = ""
    licznik = 0

    for _ in pattern:
        changed_list.append(chr(random.randint(33, 127)))
    to_change = "".join(changed_list)

    for i in range(len(splitted)):
        corrected = splitted[i].strip()
        splitted[i] = corrected
    splitted.pop()
    #
    for line in splitted:
        new_line = ""
        hs = horner(pattern, p)
        for i in range(len(line) - len(pattern) + 1):
            if hs == horner(line[i : i + len(pattern)], p):
                if naive_check(line[i : i + len(pattern)], pattern):
                    indexes.append(licznik)
                    if not new_line:
                        new_line = (
                            line[:i] + to_change + line[i + len(pattern) :]
                        )
                    else:
                        new_line = (
                            new_line[:i] + to_change + line[i + len(pattern) :]
                        )
            licznik += 1
    #
    for line in splitted:
        words = line.split()
        for i in range(len(words)):
            if words[i] == pattern:
                word_indexes.append(word_counter)
                words[i] = to_change
            word_counter += 1
        new_song += " ".join(words) + "\n"

    return indexes, new_song, word_indexes, to_change
