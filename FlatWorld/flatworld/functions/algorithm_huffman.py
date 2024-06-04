def code_song(text):
    # kodowanie
    length = len(text)
    frequency = {}

    for elem in text:
        if elem not in frequency:
            frequency[elem] = text.count(elem) / length
    frequency = dict(
        sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    )
    code = {}
    count = ""
    for elem in frequency:
        if elem == list(frequency)[-1]:
            code.update({elem: count})
        else:
            temp = "".join([count, "0"])
            code[elem] = temp
            count = "".join(["1", count])
    coded_text = ""
    for letter in text:
        coded_text = "".join([coded_text, code[letter]])

    # dekodowanie
    extract = ""
    uncoded_text = ""
    for elem in coded_text:
        extract = "".join([extract, elem])
        if extract in code.values():
            for key, value in code.items():
                if value == extract:
                    uncoded_text = "".join([uncoded_text, key])
                    extract = ""
                    break
    return code, coded_text, uncoded_text
