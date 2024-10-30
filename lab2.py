import csv
import random
import xml.etree.ElementTree as ET

# Константы
BOOKS_CSV_FILENAME = 'books.csv'
CURRENCY_XML_FILENAME = 'currency.xml'
BIBLIOGRAPHY_OUTPUT_FILE = 'bibliography.txt'
YEAR_LIMIT = 2016

# Длинные названия > 30 символов
def count_long_titles(filename):
    count = 0
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)  
        for row in reader:
            if len(row[1]) > 30:  
                count += 1
    return count

# По автору до 2016
def search_books_by_author(filename, author, year_limit=YEAR_LIMIT):
    results = {}
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            author_in_file = row['Автор (ФИО)'].strip().lower()
            input_author = author.strip().lower()

            if input_author in author_in_file:
                date_purchased = row['Дата поступления'].split()[0]  
                date_parts = date_purchased.split('.')

                if len(date_parts) == 3 and date_parts[2].isdigit():
                    try:
                        year = int(date_parts[2])  
                        if year < year_limit:
                            if row['Автор'] not in results:
                                results[row['Автор']] = []
                            results[row['Автор']].append((row['Название'], date_purchased))
                    except ValueError:
                        continue

    return results

# Реализовать генератор библиографических ссылок для 20 записей В ОТДЕЛЬНЫЙ ФАЙЛ
def generate_bibliographic_references(filename, output_file=BIBLIOGRAPHY_OUTPUT_FILE):
    references = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        all_rows = list(reader)
        sampled_rows = random.sample(all_rows, min(20, len(all_rows)))
        for row in sampled_rows:
            try:
                year = row[6].split('-')[0].split()[0]
                reference = f"{row[4]}. {row[1]} - {year}"
                references.append(reference)
            except IndexError:
                continue
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, ref in enumerate(references, start=1):
            f.write(f"{i}. {ref}\n")

# Распарсить файл и извлечь данные "Два отдельных списка Name и Value"
def parse_currency_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    
    names = []
    values = []
    
    for currency in root.findall('Valute'):
        names.append(currency.find('Name').text)
        values.append(float(currency.find('Value').text.replace(',', '.')))  # Приведение к типу float
    
    return names, values

#############################

# Подсчет длинных названий
long_titles_count = count_long_titles(BOOKS_CSV_FILENAME)
print(f"Количество записей с длинными названиями: {long_titles_count}")

print("   ")

# По автору до 2016
author_books = search_books_by_author(BOOKS_CSV_FILENAME, 'Людмила Петрановская')
for author, books in author_books.items():
    print(f"Автор: {author}")
    for book, date in books:
        print(f"  Книга: {book}, Дата поступления: {date}")
print("   ")

# Реализовать генератор библиографических ссылок для 20 записей В ОТДЕЛЬНЫЙ ФАЙЛ
generate_bibliographic_references(BOOKS_CSV_FILENAME)
print("   ")

# Распарсить файл и извлечь данные "Два отдельных списка Name и Value"
names, values = parse_currency_xml(CURRENCY_XML_FILENAME)
print(f"Имена валют: {names}")
print("   ")
print(f"Значения валют: {values}")