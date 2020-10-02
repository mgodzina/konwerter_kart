import csv
import operator

# numery grup dla kontroli dostępu
GRUPA_PELNY = 1
GRUPA_PROWADZACY = 2
GRUPA_KLUBOWICZ = 3
GRUPA_BEZDOSTEPU = 250


# konwersja numeru karty na format hex oraz dodanie nagłówka zależnego od grupy kart
def karta(numer):
    front = "0000"
    if int(numer) > 2440000 and int(numer) < 4600000:
        front = "5500"
    if int(numer) > 5860000 and int(numer) < 6000000:
        front = "8800"
    if int(numer) > 8049000 and int(numer) < 8280000:
        front = "1700"
    return front + hex(int(numer))[2:].upper()


# przypisanie do grupy na podstawie uprawnień
def grupa(row):
    if row[1] == 't' and row[2] == 't' and row[3] == 't' and row[4] == 't':
        return GRUPA_PELNY
    if row[1] == 't' and row[2] == 't' and row[3] == 't' and row[4] == 'f':
        return GRUPA_PROWADZACY
    if row[1] == 't' and row[2] == 't' and row[3] == 'f' and row[4] == 'f':
        return GRUPA_KLUBOWICZ
    return GRUPA_BEZDOSTEPU


# przypisanie numeru id użytkownika i zwiększenie licznika
def numer(row):
    global prowadzacy
    global pracownicy
    global czlonek

    if row[5] == 't':
        pracownicy += 1
        return pracownicy - 1
    if row[3] == 't' or row[4] == 't':
        prowadzacy += 1
        return prowadzacy - 1
    czlonek += 1
    return czlonek - 1


# deklaracja zmiennych
temp = []
dane_input = []
dane_output = []
# startowe numery id dla użytkowników oraz licznik
pracownicy = 10
prowadzacy = 100
czlonek = 1000

# otwarcie pliku csv i dodanie do listy
with open('kontrola_dostepu.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        # zignoruj linie nagłówka
        if line_count == 0:
            line_count += 1
        else:
            dane_input.append(row)
            line_count += 1

# sprawdzenie czy nr karty jest liczbą
for row in dane_input:
    if row[0].isdigit() == False:
        temp.append(row)

# usunięcie nieprawidłowych wpisów z listy
for row in temp:
    dane_input.remove(row)

# utworzenie listy w wyjściowym formacie
user = 1
for row in dane_input:
    dane_output.append(
        [numer(row), user, user, '', karta(row[0]), '', '48', grupa(row), 'False', 'True', '', '', '', '', '', ''])
    user += 1

# sortowanie listy
export_list = sorted(dane_output, key=operator.itemgetter(0))

# eksport do pliku csv
with open('export.csv', mode='w', newline="") as export_file:
    export_writer = csv.writer(export_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    export_writer.writerows(export_list)
