#!/usr/bin/python3

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import config
import docx  # библиотека работа в word
import nltk  # библиотека разбора текста


# print(len(doc1.paragraphs))  # количество абзацев в документе
# print(doc1.paragraphs[0].text)  # текст первого абзаца в документе
# print(doc1.paragraphs[1].text)  # текст второго абзаца в документе
# print(doc1.paragraphs[2].runs[0].text) # текст первого Run второго абзаца

# просто так функция привет )))
# def print_hi(name):
# Use a breakpoint in the code line below to debug your script.
# print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# функция удаление параграфа из документа
def delete_paragraph(paragraph):
    p = paragraph._element
    p.getparent().remove(p)
    p._p = p._element = None


# функция удаление пустых строк из документа
def strip_file(file, file_new):
    for paragraphs in file.paragraphs:
        if len(paragraphs.text) == 0:
            delete_paragraph(paragraphs)
    file.save(file_new)


# функция добавления пустых абзацев в документ
def add_par(document, par_count, new_name):
    for f in range(par_count):
        document.add_paragraph('   ')
        document.save(new_name)  # подумать как назвать файл


# функция сравнения блоков текста paragraph
def f_compare(p1, p2):
    # преобразовать каждый текст в массив предложений
    # print(len(p1), len(p2))
    if len(p1) >= len(p2):  # это чтобы из большего текста всегда вычитать меньший
        sentences1 = nltk.sent_tokenize(p1)  # массив предложений 1
        sentences2 = nltk.sent_tokenize(p2)  # массив предложений 2
    else:
        sentences1 = nltk.sent_tokenize(p2)  # массив предложений 2
        sentences2 = nltk.sent_tokenize(p1)  # массив предложений 1
    # print(sentences1,sentences2)
    res = list(set(sentences1) - set(sentences2))
    if len(res) > 0:
        # лучше не просто печатать а накапливать в массив
        print(res)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')  # тестирование работы функций

    doc1 = docx.Document(config.file1)  # линкуем первый файл как docx из конфигурационника
    doc2 = docx.Document(config.file2)  # линкуем второй файл как docx из конфигурационника

    # убрать пустые строки из файлов - это будут выровненные файлы для сравнения
    strip_file(doc1, '111.docx')  # убираем из файлов лишние строки и сохраняем под другими именами
    strip_file(doc2, '222.docx')  # убираем из файлов лишние строки и сохраняем под другими именами

    doc1 = docx.Document('111.docx')  # загружаем очищенные документы
    doc2 = docx.Document('222.docx')

    '''
    выбрать какой из подрезанных длиннее чтобы потом всегда из большего вычитать меньшее
    если больше или равно, то первый иначе второй
    '''
    if len(doc1.paragraphs) >= len(doc2.paragraphs):
        # уравнять количество параграфов путем добавления пустых параграфов в нужный жокумент
        add_par(doc2, (len(doc1.paragraphs) - len(doc2.paragraphs)),'222.docx')
        ln = len(doc1.paragraphs)
        d1 = doc1.paragraphs
        d2 = doc2.paragraphs
    else:
        # уравнять количество параграфов путем добавления пустых параграфов в нужный жокумент
        add_par(doc1, (len(doc2.paragraphs) - len(doc1.paragraphs)), '111.docx')
        ln = len(doc2.paragraphs)
        d1 = doc2.paragraphs
        d2 = doc1.paragraphs

    # print(len(doc1.paragraphs))
    # print(len(doc2.paragraphs))
    # print(ln)  # количество абзацев в самом длинном документе

    for i in range(ln-2):
        f_compare(d1[i].text, d2[i].text)  # сравниваем по параграфам
