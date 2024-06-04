import random


def generate_song():
    song = []
    words = words_list()
    print(words)
    repeated_word = random.choice(words)

    for _ in range(random.randint(2, 5)):
        vers = []
        for _ in range(5):
            word = random.choice(words)
            vers.append(word)
        vers.append(repeated_word)
        vers = " ".join(vers)
        song.append(vers)
        song.append("\n")
    song = " ".join(song)
    print(song)
    return song


def words_list():
    words = [
        "biegam",
        "piszę",
        "tańczę",
        "śpiewam",
        "oglądam",
        "gotuję",
        "czytam",
        "podróżuję",
        "pracuję",
        "śmieję się",
        "rozmawiam",
        "marzę",
        "podróżuję",
        "maluję",
        "pływam",
        "planuję",
        "gra",
        "jedzą",
        "odpoczywam",
        "trenuję",
        "oglądam",
        "podróżuję",
        "studia",
        "podróżuję",
        "robię zakupy",
        "pomagam",
        "podróżuję",
        "odpoczywam",
        "czytam",
        "komponuję",
        "dzień",
        "sen",
        "książka",
        "muzyka",
        "miłość",
        "przyjaźń",
        "podróż",
        "praca",
        "szkoła",
        "nauka",
        "dom",
        "morze",
        "góry",
        "przyroda",
        "zwierzę",
        "miasto",
        "kraj",
        "film",
        "sztuka",
        "sport",
        "zdrowie",
        "choroba",
        "przyjemność",
        "rozrywka",
        "kreatywność",
        "technologia",
        "kultura",
        "tradycja",
        "emocja",
        "uczucie",
        "piękny",
        "wspaniały",
        "ciekawy",
        "inspirujący",
        "fantastyczny",
        "niesamowity",
        "magiczny",
        "przyjemny",
        "radosny",
        "spokojny",
        "ekscytujący",
        "romantyczny",
        "aktywny",
        "kolorowy",
        "relaksujący",
        "nowoczesny",
        "tradycyjny",
        "energetyczny",
        "fascynujący",
        "dynamiczny",
        "wesoły",
        "harmonijny",
        "inspirujący",
        "pozytywny",
        "witalny",
        "wyjątkowy",
        "fantastyczny",
        "wygodny",
        "optymistyczny",
        "magiczny",
        "ja",
        "ty",
        "lubić",
    ]

    return words
