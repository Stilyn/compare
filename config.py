#!/usr/bin/python3

# файл конфигурации

symbols_clear = {} #{'.', ')', '\n'}  # символы для очистки документов перед сравнением
thresold = 88  # от 0 до 100 глубина совпадения по смыслу при сравнении абзацев документов чем меньше тем точнее

no_paragraph = 'абзац отсутствует в документе'
doc_parts_list = 'приоритет, направление, цели, задачи, программы, мероприятия, интересы'
results_folder = './compare_results/'  # папка с результатами сравнения

l2 = []
for i in range(1,100,1): l2.append(str(i)+'.')  # level 2 bullets

# словарь для распределения параграфов по уровням
doc_levels = dict(level1=['I.', 'II.', 'III.', 'IV.', 'V.', 'VI.', 'VII.', 'VIII.', 'IX.', 'X.'],
                  level2=l2,
                  level3=['а)','б)', 'в)', 'г)', 'д)', 'е)', 'ж)', 'з)', 'и)', 'к)', 'л)', 'м)', 'н)', 'о)', 'п)', 'р)', 'с)', 'т)', 'у)']
                  )