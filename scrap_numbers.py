import requests
from bs4 import BeautifulSoup
import json

# słownik przetrzymujący dane w formie pracownik: [numery]
empoyees_numbers = {}

# Zbierz ID jednostek z tagu <select>
r = requests.get('http://baza.ue.poznan.pl/index.php')
soup = BeautifulSoup(r.content, 'html.parser')
# Pierwsza opcja to 'Wybierz wszystkie', więc jej nie uwzględniamy
options = soup.select('select#departmentId option')[1:]
departments_ids = [o['value'] for o in options]
departments_ids_len = len(departments_ids)
print(f'Pobrano {departments_ids_len} ID jednostek.')

# Dla każdej jednostki zbierz numery pracowników
for index, department_id in enumerate(departments_ids[1]):
    r = requests.post('http://baza.ue.poznan.pl/index.php', data={ 'nazwisko': '', 'imie': '', 'departmentId': department_id, 'B1': 'Szukaj' })
    soup = BeautifulSoup(r.content, 'html.parser')

    # BeatifulSoup4 nie pracuje najlepiej z  baza.ue.poznan.pl (przykład w examples/parsed_index.html)
    # Więc zastosowano parę 'tricków':
    soup.select_one('html').decompose()
    soup.select_one('select').decompose()
    # Wybierz nazwy pracowników
    names_tags = soup.select('font[face="Titillium Web"][size="4"]')
    names = [n.get_text().strip() for n in names_tags]
    # Kolejny 'trick'
    soup.select_one('table').decompose()

    print(f'{(index+1):03d}/{departments_ids_len:03d} | Zbieranie numerów z jednostki o id {department_id} z {len(names)} pracownikami.')
    # Jeśli w danej jednostce pracuje chociaż jeden pracownik, zbierz numery pracowników
    if len(names) > 0:
        trs = soup.select('tr')
        current_name = names[0]
        for tr in trs:
            tr_text = tr.getText().strip()
            if (tr_text in names):
                current_name = tr_text
            else:
                if 'telefon:' in tr_text:
                    numbers = tr_text.replace('telefon:','').strip().split(', ')
                    if current_name not in empoyees_numbers:
                        empoyees_numbers[current_name] = numbers
                    else:
                        for number in numbers:
                            if number not in empoyees_numbers[current_name]:
                                empoyees_numbers[current_name].append(number)

empoyees_numbers_len = len(empoyees_numbers)
print(f'Zebrano numery {empoyees_numbers_len} pracowników')

# Dla każdego pracownika sprawdź poprawnosć numerów
if input('Wpisz "tak" aby sprawdzić poprawność numerów (może trwać kilka minut), lub "nie" aby pominąć ten krok: ') == "tak":
    success_numbers = 0
    fail_numbers = 0
    for index, employee in enumerate(empoyees_numbers):
        name_parts = employee.replace(' prof. UEP', '').split()
        print(f'{(index+1):03d}/{empoyees_numbers_len:03d} | S{success_numbers} F{fail_numbers} | Sprawdzanie poprawnosci numerów pracownika {name_parts[-1]} {name_parts[-2]}')
        r = requests.post('http://baza.ue.poznan.pl/index.php', data={ 'nazwisko': name_parts[-1], 'imie': name_parts[-2], 'departmentId': '', 'B1': 'Szukaj' })
        content = r.content
        for number in empoyees_numbers[employee]:
            if number.encode('utf-8') in content:
                success_numbers = success_numbers + 1
            else:
                fail_numbers = fail_numbers + 1
    print(f'Potwierdzono poprawność {(success_numbers/(success_numbers + fail_numbers))*100}% numerów')

f_js = open('data/data.js', 'w+')
f_js.write('const data=')
json.dump(empoyees_numbers, f_js)
json.dump(empoyees_numbers, open('data/data.json', 'w+'))
print('Dane w formacie JSON zapisano w pliku data.json oraz data.js')


