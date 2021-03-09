﻿# SDK Pullenti Lingvo, version 4.3, january 2021.
# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class MorphNumber(IntEnum):
    """ Число (единственное-множественное)
    Число
    """
    UNDEFINED = 0
    """ Неопределено """
    SINGULAR = 1
    """ Единственное """
    PLURAL = 2
    """ Множественное """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)