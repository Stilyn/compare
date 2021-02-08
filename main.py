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
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')  # тестирование работы функций
