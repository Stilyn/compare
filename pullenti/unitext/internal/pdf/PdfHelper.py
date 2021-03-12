# SDK Pullenti Unitext, version 4.3, january 2021. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import math
from pullenti.unisharp.Utils import Utils

from pullenti.unitext.internal.pdf.PdfImage import PdfImage
from pullenti.unitext.internal.pdf.PdfText import PdfText
from pullenti.unitext.UnitextContainer import UnitextContainer
from pullenti.unitext.UnitextPagebreak import UnitextPagebreak
from pullenti.unitext.UnitextPlaintext import UnitextPlaintext
from pullenti.unitext.UnitextNewline import UnitextNewline
from pullenti.unitext.internal.uni.UnilayoutHelper import UnilayoutHelper
from pullenti.unitext.UnitextDocument import UnitextDocument
from pullenti.unitext.internal.pdf.PdfFile import PdfFile
from pullenti.unitext.FileFormat import FileFormat
from pullenti.unitext.internal.pdf.PdfFig import PdfFig
from pullenti.unitext.UnilayRectangle import UnilayRectangle
from pullenti.unitext.UnilayPage import UnilayPage
from pullenti.unitext.internal.pdf.PdfPage import PdfPage

class PdfHelper:
    """ Работа с PDF """
    
    @staticmethod
    def _create_uni(pdf_file_name : str, file_content : bytearray, pars : 'CreateDocumentParam') -> 'UnitextDocument':
        pages = list()
        doc = UnitextDocument._new41(FileFormat.PDF)
        try: 
            with PdfFile() as file: 
                file.open0_(pdf_file_name, file_content)
                if (file.encrypt is not None): 
                    doc.error_message = "Can't extract pages from encrypted pdf"
                for pdic in file.pages: 
                    ppage = PdfPage(pdic)
                    up = UnilayPage()
                    up.width = (math.floor(ppage.width))
                    up.height = (math.floor(ppage.height))
                    pages.append(up)
                    up.number = len(pages)
                    for it in ppage.items: 
                        if (isinstance(it, PdfFig)): 
                            continue
                        r = UnilayRectangle()
                        r.left = it.left
                        r.top = it.top
                        r.right = it.right
                        r.bottom = it.bottom
                        r.page = up
                        if (isinstance(it, PdfText)): 
                            r.text = it.text
                        elif (isinstance(it, PdfImage)): 
                            r.image_content = it.content
                            r.tag = (it)
                        up.rects.append(r)
        except Exception as ex: 
            doc.error_message = ex.__str__()
            return doc
        if (pages is None or len(pages) == 0 or doc.error_message is not None): 
            if (doc.error_message is None): 
                doc.error_message = "Can't extract pages from pdf-file"
            return doc
        doc.pages = pages
        UnilayoutHelper.create_content_from_pages(doc, False)
        cnt = Utils.asObjectOrNull(doc.content, UnitextContainer)
        if (cnt is None): 
            return doc
        i = 0
        first_pass571 = True
        while True:
            if first_pass571: first_pass571 = False
            else: i += 1
            if (not (i < len(cnt.children))): break
            pt = Utils.asObjectOrNull(cnt.children[i], UnitextPlaintext)
            if (pt is None): 
                continue
            if (not pt.is_whitespaces): 
                continue
            if (i == 0 or (isinstance(cnt.children[i - 1], UnitextNewline)) or (isinstance(cnt.children[i - 1], UnitextPagebreak))): 
                pass
            else: 
                continue
            if ((i + 1) == len(cnt.children) or (isinstance(cnt.children[i + 1], UnitextNewline)) or (isinstance(cnt.children[i + 1], UnitextPagebreak))): 
                pass
            else: 
                continue
            del cnt.children[i]
            i -= 1
        doc.content = doc.content._optimize(True, None)
        return doc