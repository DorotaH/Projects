import pytest
from flatworld.functions.algorithm_huffman import code_song


@pytest.mark.parametrize(
    "input_text, codes, encoded, decoded",
    [
        (
            "kot ma Ale, a Ala ma kota",
            {
                " ": "0",
                "a": "10",
                "k": "110",
                "o": "1110",
                "t": "11110",
                "m": "111110",
                "A": "1111110",
                "l": "11111110",
                "e": "111111110",
                ",": "111111111",
            },
            "1101110111100111110100111111011111110111111110111111111010011111101111111010011111010011011101111010",
            "kot ma Ale, a Ala ma kota",
        ),
        (
            "Rybka musi plywac, kotek pije mleczko",
            {
                " ": "0",
                "k": "10",
                "e": "110",
                "y": "1110",
                "a": "11110",
                "m": "111110",
                "i": "1111110",
                "p": "11111110",
                "l": "111111110",
                "c": "1111111110",
                "o": "11111111110",
                "R": "111111111110",
                "b": "1111111111110",
                "u": "11111111111110",
                "s": "111111111111110",
                "w": "1111111111111110",
                ",": "11111111111111110",
                "t": "111111111111111110",
                "j": "1111111111111111110",
                "z": "1111111111111111111",
            },
            "111111111110111011111111111101011110011111011111111111110111111111111110111111001111111011111111011101111111111111110111101111111110111111111111111100101111111111011111111111111111011010011111110111111011111111111111111101100111110111111110110111111111011111111111111111111011111111110",
            "Rybka musi plywac, kotek pije mleczko",
        ),
    ],
)
def test_huffman(input_text, codes, encoded, decoded):
    text = input_text
    huffman_code, huffman_coded_text, huffman_uncoded_text = code_song(text)
    print(huffman_code, huffman_coded_text, huffman_uncoded_text)
    assert codes == huffman_code
    assert encoded == huffman_coded_text
    assert decoded == huffman_uncoded_text
