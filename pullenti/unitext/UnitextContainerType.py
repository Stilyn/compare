# SDK Pullenti Unitext, version 4.3, january 2021. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class UnitextContainerType(IntEnum):
    """ Тип контейнера элементов """
    UNDEFINED = 0
    """ Обычный контейнер """
    SHAPE = 1
    """ Контейнер является полотном с визуальными формами
    (прямоугольник, форма, круг ...), которые содержат тексты """
    CONTENTCONTROL = 2
    """ Это для MSWord элемент управления содержимым """
    MONOSPACE = 3
    """ Содержимое рекомендуется выводиться моноширинным шрифтом,
    так как содержит разную псевдографику """
    HIGHLIGHTING = 4
    """ Временная подсветка """
    KEYWORD = 5
    """ Ключевое слово (например, Статья или Глава) """
    NUMBER = 6
    """ Нумерация раздела (блока) """
    NAME = 7
    """ Наименование раздела """
    EDITION = 8
    """ Указания редакций (например,  п.1 в ред. ФЗ-123) """
    COMMENT = 9
    """ Это некоторый внешний комментарий """
    DIRECTIVE = 10
    """ Это ключевое слово типа "Приказываю:" ... """
    URL = 11
    """ Вычисленный в ходе анализа URL (Data - сам URL). Это не обязательно в чистом
    виде URL, а может быть ссылка на НПА, литературу и т.п. """
    HEAD = 12
    """ Заголовок блока текста (см. UnitextDocblock) """
    TAIL = 13
    """ Подпись блока текста (см. UnitextDocblock) """
    RIGHTALIGN = 14
    """ Это некоторый участок, выравниваемый вправо
    (например, в записке в заголовке - кому и от кого) """
    ENTITY = 15
    """ Некоторая сущность """
    USERTYPE = 16
    """ Некоторый пользовательский тип """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)