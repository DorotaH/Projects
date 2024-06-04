
# Zespół nr: 1
Skład zespołu wraz z funkcjami:<br />

Dorota Harasimiuk - sekretarz<br />
Jakub Obarowski – przywódca<br />
Marcel Tutak - zastępca<br /><br />
![kraina](https://github.com/obarowskij/AiSD/assets/146991219/70d9dfba-e964-468b-bb6d-59a82b36d572)

# Wystartowanie projektu

## Krok 1.
pobranie paczki requirements
```bash
pip install -r requirements.txt
```

## Krok 2.
Migracje
```bash
python manage.py migrate
```

## Krok 3.
Uruchomienie aplikacji
```bash
python manage.py runserver
```
Serwer uruchomi się domyślnie pod adresem http://127.0.0.1:8000

## Uruchomienie Testów
```bash
pytest
```

# Dokumentacja
| L.p | Specyfikacja problemu (dane i wyniki) | Do jakich treści w zadaniu odnosi się algorytm | Zastosowane struktury danych | Informacje o zastosowanym algorytmie |
| --- | -------------------------------------- | --------------------------------------------- | ---------------------------- | ----------------------------------- |
| 1.  | Dane: zbiór punktów orientacyjnych tworzących obszar Krainy <br /> Wynik: bliczenie otoczki wypukłej Krainy | Zdefiniowanie obszaru w którym żyją płaszczaki na Stronie | stos, klasa, listy | Algorytm Grahama - wpierw losujemy punkty obserwacyjne i sortujemy je biegunowo. Później wkładamy je na stos i mamy gotową wypukłą otoczkę, którą zwizualiujemy biblioteką matplotlib |
| 2.  | Dane: Tragarze przedstawieni jako punkty w przestrzeni, gdzie każdy tragarz reprezentowany jest przez dwa punkty (np. jeden punkt to położenie tragarza, a drugi to położenie jego rąk, przy założeniu pewnej ustalonej odległości między nimi)<br /> Wynik: Lista tragarzy, którzy mogą współpracować ze sobą przy transporcie odcinków z fabryki | Dobranie tragarzy do transportu odcinków z fabryki | listy? | Geometria obliczeniowa na płaszczyźnie |
| 3.  | Dane: Otoczka wypukła Krainy oraz lista tragarzy gotowych do współpracy<br /> Wynik: Minimalny czas potrzebny do zbudowania płotu wokół Krainy | Zbudowanie płotu wokół Krainy | kolejka, klasa | Mając otoczkę grahama przedstawiamy to jako sieć przepływową i aby znaleźć, ile razy płaszczaki muszą się zbierać do budowy płotu, możemy użyć algorytmu Forda-Fulkersona, aby znaleźć maksymalny przepływ z punktu źródłowego (gdzie zaczynają się prace budowlane) do punktu ujściowego (gdzie prace się kończą), uwzględniając ograniczenia przepustowości na krawędziach. Ostatecznie, maksymalny przepływ w tej sieci przepływowej będzie reprezentować maksymalną liczbę tragarzy, które mogą być przenoszone od fabryki do miejsca budowy płotu, co pośrednio może odzwierciedlać, ile razy płaszczaki muszą się zbierać, aby zbudować płot. |
| 4.  | Dane: Ciąg znaków reprezentujący zmienioną melodię (opowieść-melodia) oraz ciąg znaków zawierający zmienioną wersję melodi, gdzie jedna litera została zastąpiona przez inną (koszmarna-melodia)<br /> Wynik: Oryginalna melodia | Znalezienie oryginalnej melodii | Lista | Algorytm Rabina-Karpa, Algorytm KMP |
| 5.  | Dane: Ciąg znaków a1a2...an reprezentujący opowieść-melodię<br /> Wynik: Ustalenie kodowania dla ciągu znaków, umożliwiającego kompresję danych | Problem niewystarczającej ilości pamięci na komputerze informatyka płaszczaka | słowniki | Huffman - polega na analizie częstotliwości występowania liter w zdaniu i na tej podstawie przypisywaniu skróconych kodów dla symboli |
| 6.  | Dane: opowieść-melodia <br /> Wynik: indeks potencjalnego podmienionego znaku w melodii | ewentualnej zamiana innych fragmentów opowieści-melodii | ----------- | ----------- |
| 7.  | Dane: Lista strażników <br /> Wynik: Harmonogram pracy strażników ustawiany według minimalnej liczby odsłuchań melodii w trakcie pracy | Potrzeba ochrony płotu | ----------- | ----------- |

