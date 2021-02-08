#!/usr/bin/python3

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import config
import docx  # библиотека работа в word
import nltk  # библиотека разбора текста

doc1 = docx.Document(config.file1)  # линкуем первый файл из конфигурационника
doc2 = docx.Document(config.file2)  # линкуем второй файл из конфигурационника


# print(len(doc1.paragraphs))  # количество абзацев в документе
# print(doc1.paragraphs[0].text)  # текст первого абзаца в документе
# print(doc1.paragraphs[1].text)  # текст второго абзаца в документе
# print(doc1.paragraphs[2].runs[0].text) # текст первого Run второго абзаца

# просто так функция привет )))
#def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    # print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# функция сравнения блоков текста paragraph
def f_compare(p1, p2):
    # преобразовать каждый текст в массив предложений
    sentences1 = nltk.sent_tokenize(p1)
    sentences2 = nltk.sent_tokenize(p2)
    for sentence1 in sentences1:
        for sentence2 in sentences2:
            #print(sentence1)
            #print(sentence2)
            if (sentence1 > sentence2):
                print('Разница документа 1 ******* \n' + sentence2)
                # break
            elif (sentence2 > sentence1):
                print('Разница документа 2 ******* \n' + sentence1)
                break
            else:
                break

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')  # тестирование работы функций
    # убрать пустые строки из файлов

    # выбрать какой длиннее
    # запустить цикл сравнения с наибольшей длиной
    i = 0
    while i < len(doc1.paragraphs):
        f_compare(doc1.paragraphs[i].text, doc2.paragraphs[i].text)
        i = i + 1

