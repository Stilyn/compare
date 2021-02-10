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


# функция сравнения блоков текста paragraph
def f_compare(p1, p2):
    # преобразовать каждый текст в массив предложений
    sentences1 = nltk.sent_tokenize(p1)  # массив предложений 1
    sentences2 = nltk.sent_tokenize(p2)  # массив предложений 2
    print(list(set(sentences1)-set(sentences2)))



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')  # тестирование работы функций

    doc1 = docx.Document(config.file1)  # линкуем первый файл из конфигурационника
    doc2 = docx.Document(config.file2)  # линкуем второй файл из конфигурационника

    # убрать пустые строки из файлов

    # убрать точки и заменить на пробелы

    # выбрать какой длиннее чтобы потом всегда из большего вычитать меньшее
    if len(doc1.paragraphs) > len(doc2.paragraphs):
        ln = len(doc1.paragraphs)
        d1 = doc1.paragraphs
        d2 = doc2.paragraphs
    else:
        ln = len(doc2.paragraphs)
        d1 = doc2.paragraphs
        d2 = doc1.paragraphs
    # print(ln)

    # запустить цикл сравнения с наибольшей длиной
    i = 0
    while i < ln:  #
        f_compare(d1[i].text, d2[i].text)  # сравниваем по параграфам
        # а если добавили лишний раздел????????
        i = i + 1
        # doc1.add_paragraph('ass'); # добавляем новый параграф
        # doc1.save('111.docx') # сохраняем файл
