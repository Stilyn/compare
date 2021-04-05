#!/usr/bin/python3

# файл конфигурации

symbols_clear = {} #{'.', ')', '\n'}  # символы для очистки документов перед сравнением
thresold = 88  # от 0 до 100 глубина совпадения по смыслу при сравнении абзацев документов чем меньше тем точнее

no_paragraph = 'абзац отсутствует в документе'
doc_parts_list = 'приоритет, направление, цели, задачи, программы, мероприятия'
results_folder = './compare_results/'  # папка с результатами сравнения