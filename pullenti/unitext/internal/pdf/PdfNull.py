﻿# SDK Pullenti Unitext, version 4.3, january 2021. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.unitext.internal.pdf.PdfObject import PdfObject

class PdfNull(PdfObject):
    
    def to_string(self, lev : int) -> str:
        return "NULL"
    
    def is_simple(self, lev : int) -> bool:
        return True