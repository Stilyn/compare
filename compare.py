#!/usr/bin/python3

'''
Пример запуска из командной строки
python3 compare.py Основы.docx Основы2.docx
'''

# imports
import sys
import os
import config
import docx  # библиотека работа в word
from docx import Document
from docx.shared import Inches
from docx.shared import RGBColor
from docx.enum.text import WD_COLOR
import nltk  # библиотека разбора текста
import string
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from diff_match_patch import diff_match_patch as diff_module  # для сравнения и раскраски по совету коллег
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import jinja2
from jinja2 import Template, Environment, FileSystemLoader
import jinja2
from jinja2 import Template, Environment, FileSystemLoader

# ********************************************смысловой разбор и поиск ключевых слов
import pullenti_wrapper
from pullenti_wrapper.langs import (set_langs, RU, EN)

set_langs([RU, EN])

from pullenti_wrapper.processor import (Processor, DATE, GEO, ORGANIZATION, PERSON, MONEY, ADDRESS)

processor = Processor([DATE, GEO, ORGANIZATION, PERSON, MONEY, ADDRESS])


def zart_flatten(a): # a - многовложенный list с неопределенной глубиной
    """
    Non recursive algorithm
    Based on pop from old and append elements to new list
    """
    queue, out = [a], []
    while queue:
        elem = queue.pop(-1)
        if isinstance(elem, list):
            queue.extend(elem)
        else:
            out.append(elem)
    return out[::-1]

def mind_generate(text):
    mind = processor(text)
    mslots = {}  # делаем словарь ключевых слов
    # print(mind.text)
    # print(mind.matches)  # это список
    for jp in mind.walk():
        label = jp.referent.label
        #slots = jp.referent.slots
        children = jp.referent.children
        mslots.update({label: label})
        for d in jp.referent.slots:
            mslots.update({d.key: d.value})
    return mslots.values()  # возвращает список ключевых слов файла


# ********************************************смысловой разбор и поиск ключевых слов


# функция переименования файлов для формирования временных
def file_rename(file_name):
    n = file_name.split('.')[0] + '_vs' + '.docx'
    return str(n)


# функция удаление параграфа из документа
def delete_paragraph(paragraph):
    p = paragraph._element
    p.getparent().remove(p)
    p._p = p._element = None


# функция удаление пустых параграфов из документа
def strip_file(file, file_new):
    for paragraphs in file.paragraphs:
        if len(paragraphs.text) == 0:
            delete_paragraph(paragraphs)
    file.save(file_new)


# функция добавления пустых абзацев в документ
def add_par(document, par_count, new_name):
    for f in range(par_count):
        document.add_paragraph(' ')
        document.save(new_name)  # подумать как назвать файл


# функция разбивки русского текста на слова
def tokenize_ru(file_text):
    # firstly let's apply nltk tokenization
    tokens = word_tokenize(file_text)

    # let's delete punctuation symbols
    tokens = [i for i in tokens if (i not in string.punctuation)]

    # deleting stop_words
    stop_words = stopwords.words('russian')
    # stop_words = []
    stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', '–', 'к', 'на', '...'])
    tokens = [i for i in tokens if (i not in stop_words)]

    # cleaning words
    tokens = [i.replace("«", "").replace("»", "") for i in tokens]

    return tokens


# функция поиска смыслового совпадения параграфов глубина threshold
def par_match(p1, p2, thresold):
    dmp = diff_module()
    diff_module.Match_Threshold = thresold
    # diff_module.Match_Distance = 0
    matches = dmp.match_main(p1, p2, 0)
    return matches


# функция сравнения блоков текста paragraph
def f_compare(p1, p2):
    # чистим абзацы от шлака
    for k in config.symbols_clear:
        p1 = str.replace(p1, k, ' ')
        p2 = str.replace(p2, k, ' ')

    dmp = diff_module()
    diffs = dmp.diff_main(p1, p2)  # разница
    # dmp.diff_cleanupSemantic(diffs)
    # вот здесь нужно значительно улучшить алгоритм сравнения
    return dmp.diff_prettyHtml(diffs)


def color_paragraph(paragraph):
    # paragraphs.runs[s].font.color.rgb = RGBColor(0xff, 0x00, 0x00) # красный текст после нуля просто цвет html
    # paragraphs.runs[s].font.bold = True # жирный шрифт
    paragraph.style.font.highlight_color = WD_COLOR.YELLOW  # цвет выделения желтый


'''для использования отладочного и боевого режимов'''

if len(sys.argv) > 1:  # если из под командной строки запускаем
    print('сравниваю ' + sys.argv[1] + ' и ' + sys.argv[2])
    file1 = sys.argv[1]
    file2 = sys.argv[2]
else:
    print('отладочный режим')  # если не из под командной строки запускаем
    file1 = '906_2013.docx'
    file2 = '64_2020.docx'

doc1 = docx.Document(file1)  # линкуем первый файл как docx из конфигурационника
doc2 = docx.Document(file2)  # линкуем второй файл как docx из конфигурационника

# убрать пустые строки из файлов - это будут выровненные файлы для сравнения
strip_file(doc1, file_rename(file1))  # убираем из файлов лишние строки и сохраняем под другими именами
strip_file(doc2, file_rename(file2))  # убираем из файлов лишние строки и сохраняем под другими именами

'''
загружаем очищенные документы
file_rename(file1) это имя переименованного файла 1
file_rename(file2) это имя переименованного файла 2
'''
doc1 = docx.Document(file_rename(file1))
doc2 = docx.Document(file_rename(file2))
q1 = []  # очищенные списки для вывода html 1 документа
q2 = []  # очищенные списки для вывода html 2 документа
q3 = []  # процент совпадения

# print(len(doc1.paragraphs), len(doc2.paragraphs))

# уравниваем количество параграфов в документах
# if len(doc1.paragraphs) > len(doc2.paragraphs):
#    add_par(doc2, (len(doc1.paragraphs) - len(doc2.paragraphs)), file_rename(file2))
# if len(doc2.paragraphs) > len(doc1.paragraphs):
#    add_par(doc1, (len(doc2.paragraphs) - len(doc1.paragraphs)), file_rename(file1))

print(len(doc1.paragraphs), len(doc2.paragraphs))

# создаем файл docx с результатами сравнения
file_compare_name_d = file1.split('.')[0] + '_vs_' + file2.split('.')[0] + '.docx'
# print(file_compare_name_d)

doc3 = Document()  # создаем новый docx куда поместим результаты сравнения
with open(file_compare_name_d, 'w') as f2:
    # создаем таблицу и шапку
    table = doc3.add_table(rows=1, cols=3)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = file_rename(file1)
    hdr_cells[1].text = '%'
    hdr_cells[2].text = file_rename(file2)
    for i in doc1.paragraphs:  # берем все параграфы документа 1
        i_mind = mind_generate(i.text)
        # print(doc1.paragraphs[i].text)
        for j in doc2.paragraphs:
            j_mind = mind_generate(j.text)
            print('********** 1 *********************')
            print(i_mind)
            print('********** 2 *********************')
            print(j_mind)
            print('********** % *********************')
            a = fuzz.WRatio(' '.join(tokenize_ru(i.text)),
                            ' '.join(tokenize_ru(j.text)))  # ищем совпадение по смыслу в %
            print(a)
            if a >= config.thresold:
                # готовим данные для html
                q1.append(i.text)  # сразу добавляем абзац документа 1 в html
                # q2.append(f_compare(i.text, j.text))  # разница между 2 и 1 доком
                q2.append(j.text)  # разница между 2 и 1 доком
                q3.append(a)  # сразу добавляем для html
                row_cells = table.add_row().cells  # добавляем данные в строку таблицы docx
                row_cells[0].text = i.text  # сразу добавляем абзац документа 1 в docx
                row_cells[1].text = str(a)  # и для docx
                row_cells[2].text = j.text  # потом неплохо было бы их раскрасить
            else:
                # q1.append(i.text)  # сразу добавляем абзац документа 1 в html
                # q2.append(config.no_paragraph)  # добавляем пустышку
                # q3.append(a)  # сразу добавляем для html
                # row_cells[1].text = str(a)  # и для docx
                # row_cells[2].text = config.no_paragraph   # потом неплохо было бы их раскрасить
                continue
    doc3.save(file_compare_name_d)  # сохраняем файл docx
    f2.close()
print(len(q1), len(q2), len(q3))
# создаем файл html с результаттми сравнения
file_compare_name = file1.split('.')[0] + '_vs_' + file2.split('.')[0] + '.html'
# запись в файл
curr_dir = os.path.dirname(os.path.abspath(__file__))  # указываем что шаблон находится в корне
env = Environment(loader=FileSystemLoader(curr_dir))  # подгружаем шаблон из текущей папки
template = env.get_template('template.html')
print(len(q1), len(q2), len(q3))
with open(file_compare_name, "w", encoding='utf-8') as f:
    f.write(template.render(file_name1=file_rename(file1), file_name2=file_rename(file2), q1=q1, q2=q2, q3=q3,
                            len=max(len(q1), len(q2), len(q3))))
f.close()
