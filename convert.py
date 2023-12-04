import csv
import operator
from datetime import date
import glob
import os


GRUPA_PELNY = 1
GRUPA_ROZSZEZONY = 4
GRUPA_PROWADZACY = 2
GRUPA_KLUBOWICZ = 3
GRUPA_BEZDOSTEPU = 250
dostep_pelny = 0
dostep_rozszezony = 0
dostep_prowadzacy = 0
dostep_klubowicz = 0



def karta(numer):
    front= ""
    if int(numer) > 11000000 and int(numer) < 12000000:
        front = "1D00"
    if int(numer) > 2440000 and int(numer) < 4600000:
        front = "5500"
    if int(numer) > 3000000 and int(numer) < 3170000:
        front = "1C00"
    if int(numer) > 5860000 and int(numer) < 6000000:
        front = "8800"
    if int(numer) > 7400000 and int(numer) < 7600000:
        front = "3100"
    if int(numer) > 8049000 and int(numer) < 8280000:
        front = "1700"
    return front+hex(int(numer))[2:].upper()

def grupa(row):
    global dostep_pelny
    global dostep_rozszezony
    global dostep_prowadzacy
    global dostep_klubowicz
    if row[5] == 't':
        dostep_pelny += 1
        return GRUPA_PELNY
    if row[1] == 't' and row[2] == 't' and row[3] == 't' and row[4] == 't':
        dostep_rozszezony += 1
        return GRUPA_ROZSZEZONY
    if row[1] == 't' and row[2] == 't' and row[3] == 't' and row[4] == 'f':
        dostep_prowadzacy += 1
        return GRUPA_PROWADZACY
    if row[1] == 't' and row[2] == 't' and row[3] == 'f' and row[4] == 'f':
        dostep_klubowicz += 1
        return GRUPA_KLUBOWICZ
    return 0;

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
    return  czlonek - 1

temp = []
dane_input = []
dane_output = []
pracownicy = 100
prowadzacy = 250
czlonek = 1000
user = 1

list_of_files = glob.glob('C:\\Users\\KSI\\Downloads\\kontrola_dostepu*.csv') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)


with open(latest_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            dane_input.append(row)
            line_count += 1
print(f'Processed {line_count} lines from data input')
print(f'No. of corrent entries {len(dane_input)} lines.')

with open('stale.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            dane_input.append(row)
            line_count += 1
print(f'Processed {line_count} lines from constant data input')
print(f'No. of corrent entries {len(dane_input)} lines.')


for row in dane_input:
    if row[0].isdigit() == False:
        temp.append(row)

for row in temp:
    dane_input.remove(row)

for row in dane_input:
    dane_output.append([numer(row), str(user), str(user),'', karta(row[0]),'','48', grupa(row),'False','True','','','','','',''])
    user += 1
    
with open('switcher.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        dane_output.append([int(row[0]), row[1], row[1],'', str(row[2]),'','48', GRUPA_PELNY,'False','True','','','','','',''])

print(f'No. of pracownicy = {pracownicy - 100}')
print(f'No. of full access  = {dostep_pelny}')
print(f'No. of rusznikarnia access  = {dostep_rozszezony}')
print(f'No. of 15m access = {dostep_prowadzacy}')
print(f'No. of normal access = {dostep_klubowicz}')

export=sorted(dane_output, key=operator.itemgetter(0))


today = date.today()
exportfilename = today.strftime("export%Y%m%d.csv")


with open(exportfilename, mode='w', newline="") as employee_file:
    employee_writer = csv.writer(employee_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    employee_writer.writerows(export)

input()
