#!/usr/bin/python3

'''
Пример запуска из командной строки
python3 compare.py Основы.docx Основы2.docx
'''

# imports
import sys
import config
import docx  # библиотека работа в word
from docx import Document
from docx.shared import RGBColor
from docx.enum.text import WD_COLOR
import nltk  # библиотека разбора текста
import string
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from diff_match_patch import diff_match_patch as diff_module  # для сравнения и раскраски по совету коллег


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


# функция поиска смыслового совпадения параграфов глубина Match threshold: 0,6
def par_match(p1,p2, thresold):
    dmp = diff_module()
    diff_module.Match_Threshold = thresold
    matches = dmp.match_main(p1,p2,(len(p1)//3))
    #if matches != -1:
        # print(p1,p2)
    #    print(matches)
    return matches

# функция сравнения блоков текста paragraph
def f_compare(p1, p2):
    # чистим абзацы от шлака
    for k in config.symbols_clear:
        p1 = str.replace(p1, k, ' ')
        p2 = str.replace(p2, k, ' ')

    dmp = diff_module()
    diffs = dmp.diff_main(p1, p2)  # разница
    dmp.diff_cleanupSemantic(diffs)

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
    file1 = 'Основы2020.docx'
    file2 = 'Основы2030.docx'

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

html_body = ''  # наш будущий html для сравнения
for i in range(len(doc1.paragraphs)):
    # найти смысловое совпадение параграфов из 2 документа c параграфами 1 документа
    for j in range(len(doc2.paragraphs)):
        a = par_match(doc1.paragraphs[i].text, doc2.paragraphs[j].text, 0.8)  #ищем смысловое совпадание
        if a > 0:
            print(a)
            #txt_doc1 = ' '.join(nltk.sent_tokenize(doc1.paragraphs[i].text, 'russian'))
            #txt_doc2 = ' '.join(nltk.sent_tokenize(doc2.paragraphs[i].text, 'russian'))
            html_body = html_body +'<br><br><br><br>'+ f_compare(doc1.paragraphs[i].text, doc2.paragraphs[j].text)  # дописываем в телло результат сравнения очередного параграфа
            # print(html_body)
    # txt_doc1 = txt_doc1 + ' '.join(nltk.sent_tokenize(doc1.paragraphs[i].text, 'russian')) + '\n'  # полный текст первого документа
    # txt_doc2 = txt_doc2 + ' '.join(nltk.sent_tokenize(doc2.paragraphs[i].text, 'russian')) + '\n'  # полный текст второго документа
    # html дописываем в тело html
    #html_body += f_compare(txt_doc1, txt_doc2) # дописываем в телло результат сравнения очередного параграфа
# print(txt_doc2)
# проверять что предложение входит
html_compare = config.html_start + html_body + config.html_end  # делает html
file_compare_name = file1.split('.')[0] + '_vs_' + file2.split('.')[0] + '.html'
f = open(file_compare_name, 'w')
f.write(html_compare)
