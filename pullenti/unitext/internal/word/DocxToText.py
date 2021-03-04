# SDK Pullenti Unitext, version 4.3, january 2021. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import xml.etree
import base64
import io
import typing
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.uni.IUnitextGenNumStyle import IUnitextGenNumStyle
from pullenti.unitext.internal.word.DocTable import DocTable
from pullenti.unitext.UnitextContainerType import UnitextContainerType
from pullenti.unitext.UnitextHyperlink import UnitextHyperlink
from pullenti.unitext.internal.misc.ExcelHelper import ExcelHelper
from pullenti.unitext.internal.misc.WingdingsHelper import WingdingsHelper
from pullenti.unitext.UnitextPlaintextType import UnitextPlaintextType
from pullenti.unitext.internal.uni.UniTextGenNumLevel import UniTextGenNumLevel
from pullenti.unitext.internal.uni.UnitextGenNumStyleEx import UnitextGenNumStyleEx
from pullenti.unitext.internal.uni.UniTextGenNumType import UniTextGenNumType
from pullenti.unitext.UnitextPlaintext import UnitextPlaintext
from pullenti.unitext.UnitextFootnote import UnitextFootnote
from pullenti.unitext.internal.uni.UnitextGenNumStyle import UnitextGenNumStyle
from pullenti.unitext.internal.misc.MyXmlReader import MyXmlReader
from pullenti.unitext.internal.word.DocxPart import DocxPart
from pullenti.unitext.internal.uni.UnitextHelper import UnitextHelper
from pullenti.unitext.UnitextImage import UnitextImage
from pullenti.unitext.internal.uni.UnitextGen import UnitextGen
from pullenti.unitext.UnitextComment import UnitextComment
from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.FileFormat import FileFormat
from pullenti.unitext.internal.misc.MyZipFile import MyZipFile
from pullenti.unitext.UnitextContainer import UnitextContainer
from pullenti.unitext.UnitextPagebreak import UnitextPagebreak
from pullenti.unitext.UnitextService import UnitextService
from pullenti.unitext.UnitextDocument import UnitextDocument
from pullenti.unitext.internal.misc.OdtHelper import OdtHelper
from pullenti.unitext.internal.misc.BorderInfo import BorderInfo

class DocxToText(object):
    
    class UnitextTextStyle:
        
        def __init__(self) -> None:
            self.name = None;
            self.aliases = None;
            self.upper_case = False
            self.num_id = None;
            self.num_lvl = 0
        
        @property
        def is_heading(self) -> bool:
            if (self.name is not None): 
                if (Utils.startsWithString(self.name, "head", True)): 
                    return True
            if (self.aliases is not None): 
                if (Utils.startsWithString(self.aliases, "head", True)): 
                    return True
                if ("аголовок" in self.aliases): 
                    return True
            return False
        
        def __str__(self) -> str:
            return self.name
    
    def __init__(self, file_name : str, content : bytearray, is_xml : bool) -> None:
        self.__zip_file = None
        self.__xml_file = None
        self.__parts = list()
        self.__m_hyperlinks = dict()
        self.__m_data_controls = dict()
        self.__m_comments = dict()
        self.__m_embeds = dict()
        self.__m_lastrsid = ""
        self.__m_last_char = ' '
        self.__m_footnotes = dict()
        self.__m_text_styles = dict()
        self.__m_num_styles = dict()
        if (is_xml): 
            self.__xml_file = None # new XmlDocument
            if (content is not None): 
                with MemoryStream(content) as mem: 
                    self.__xml_file = Utils.parseXmlFromStream(mem)
            else: 
                with FileStream(file_name, "rb") as fs: 
                    self.__xml_file = Utils.parseXmlFromStream(fs)
            self.__prepare_xml()
        else: 
            self.__zip_file = MyZipFile(file_name, content)
            self.__prepare_zip()
    
    def __prepare_zip(self) -> None:
        for o in self.__zip_file.entries: 
            if (o.is_directory or o.encrypted or o.data_size == 0): 
                continue
            self.__parts.append(DocxPart._new397(o.name, o))
    
    def __prepare_xml(self) -> None:
        if (Utils.getXmlLocalName(self.__xml_file.getroot()) == "wordDocument"): 
            self.__parts.append(DocxPart._new398("word/document.xml", self.__xml_file.getroot()))
            return
        for xml0_ in self.__xml_file.getroot(): 
            if (Utils.getXmlLocalName(xml0_) == "part"): 
                p = DocxPart()
                if (xml0_.attrib is not None): 
                    for a in xml0_.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "name"): 
                            p.name = a[1]
                            if (p.name.startswith("/")): 
                                p.name = p.name[1:]
                            break
                for x in xml0_: 
                    if (Utils.getXmlLocalName(x) == "xmlData"): 
                        for xx in x: 
                            p.xml0_ = xx
                            break
                        break
                    elif (Utils.getXmlLocalName(x) == "binaryData"): 
                        try: 
                            p.data = base64.decodestring((Utils.getXmlInnerText(x)).encode('utf-8', 'ignore'))
                        except Exception as ex: 
                            pass
                        break
                if (p.name is not None and ((p.xml0_ is not None or p.data is not None))): 
                    self.__parts.append(p)
    
    def close(self) -> None:
        try: 
            if (self.__zip_file is not None): 
                self.__zip_file.close()
                self.__zip_file = (None)
        except Exception as ex: 
            pass
    
    def create_uni_doc(self, only_for_pure_text : bool, frm : 'FileFormat', pars : 'CreateDocumentParam') -> 'UnitextDocument':
        headers = list()
        footers = list()
        sheets = dict()
        id_images = dict()
        id_embeds = dict()
        shared_strings = list()
        cell_borders = dict()
        ppt_slides = dict()
        ppt_images = dict()
        xml_doc = None
        xml_book = None
        xml_comments = None
        xml_footnotes = None
        xml_endnotes = None
        xml_odt_content = None
        xml_odt_style = None
        for p in self.__parts: 
            if (p.is_name("word/document.xml")): 
                xml_doc = p.get_xml_node(False)
            elif (p.is_name("word/footnotes.xml")): 
                xml_footnotes = p.get_xml_node(False)
            elif (p.is_name("word/endnotes.xml")): 
                xml_endnotes = p.get_xml_node(False)
            elif (p.is_name("word/styles.xml")): 
                self.__read_text_styles(p.get_xml_node(False))
            elif (p.is_name("word/comments.xml")): 
                xml_comments = p.get_xml_node(False)
                if (xml_comments is not None): 
                    for x in xml_comments: 
                        if (Utils.getXmlLocalName(x) == "comment"): 
                            cmt = UnitextComment()
                            id0_ = None
                            if (x.attrib is not None): 
                                for a in x.attrib.items(): 
                                    if (Utils.getXmlAttrLocalName(a) == "id"): 
                                        id0_ = a[1]
                                    elif (Utils.getXmlAttrLocalName(a) == "author"): 
                                        cmt.author = a[1]
                            if (id0_ is None or id0_ in self.__m_comments): 
                                continue
                            gen = UnitextGen()
                            xxx = list()
                            xxx.append(x)
                            self._read_node(xxx, gen, None, -1)
                            it = gen.finish(True, None)
                            if (it is not None): 
                                tmp = io.StringIO()
                                it.get_plaintext(tmp, None)
                                if (tmp.tell() > 0): 
                                    cmt.text = Utils.toStringStringIO(tmp)
                                    self.__m_comments[id0_] = cmt
            elif (p.is_name("content.xml")): 
                xml_odt_content = p.get_xml_node(True)
            elif (p.is_name("styles.xml")): 
                xml_odt_style = p.get_xml_node(True)
            elif (p.is_name("xl/workbook.xml")): 
                xml_book = p.get_xml_node(False)
            elif (p.is_name("xl/sharedStrings.xml")): 
                xml0_ = p.get_xml_node(False)
                if (xml0_ is not None): 
                    for xx in xml0_: 
                        if (Utils.getXmlLocalName(xx) == "si"): 
                            gg = UnitextGen()
                            xxx = list()
                            xxx.append(xx)
                            self._read_node(xxx, gg, None, -1)
                            shared_strings.append(gg.finish(True, None))
            elif (p.is_name("xl/styles.xml")): 
                xml0_ = p.get_xml_node(False)
                if (xml0_ is not None): 
                    brdr = list()
                    for xx in xml0_: 
                        if (Utils.getXmlLocalName(xx) == "borders"): 
                            for xxx in xx: 
                                if (Utils.getXmlLocalName(xxx) == "border"): 
                                    brd = BorderInfo()
                                    brdr.append(brd)
                                    for y in xxx: 
                                        if (len(y.attrib) > 0 or len(y) > 0): 
                                            if (Utils.getXmlLocalName(y) == "left"): 
                                                brd.left = True
                                            elif (Utils.getXmlLocalName(y) == "right"): 
                                                brd.right = True
                                            elif (Utils.getXmlLocalName(y) == "top"): 
                                                brd.top = True
                                            elif (Utils.getXmlLocalName(y) == "bottom"): 
                                                brd.bottom = True
                        elif (Utils.getXmlLocalName(xx) == "cellXfs"): 
                            nu = 0
                            for xxx in xx: 
                                if (Utils.getXmlLocalName(xxx) == "xf"): 
                                    ind = 0
                                    if (xxx.attrib is not None): 
                                        for a in xxx.attrib.items(): 
                                            if (Utils.getXmlAttrLocalName(a) == "borderId"): 
                                                wrapind399 = RefOutArgWrapper(0)
                                                Utils.tryParseInt(a[1], wrapind399)
                                                ind = wrapind399.value
                                                break
                                    if (ind >= 0 and (ind < len(brdr))): 
                                        cell_borders[str(nu)] = brdr[ind]
                                    nu += 1
            elif (((p.is_name_starts("word/_rels/") or p.is_name_starts("xl/_rels/") or p.is_name_starts("ppt/slides/_rels/"))) and ((p.zip_entry is not None and not p.zip_entry.is_directory))): 
                xml_rels = p.get_xml_node(False)
                if (xml_rels is not None): 
                    ppt_imgs = None
                    if (p.name.startswith("ppt")): 
                        ii = p.name.find("rels/slide")
                        if (ii < 0): 
                            continue
                        nam = p.name[ii + 10:]
                        ii = nam.find('.')
                        if (ii < 0): 
                            continue
                        wrapii400 = RefOutArgWrapper(0)
                        inoutres401 = Utils.tryParseInt(nam[0:0+ii], wrapii400)
                        ii = wrapii400.value
                        if (not inoutres401): 
                            continue
                        if (ii in ppt_images): 
                            continue
                        ppt_imgs = dict()
                        ppt_images[ii] = ppt_imgs
                    for xx in xml_rels: 
                        if (xx.attrib is not None): 
                            if (Utils.getXmlAttrByName(xx.attrib, "Id") is not None and Utils.getXmlAttrByName(xx.attrib, "Target") is not None and Utils.getXmlAttrByName(xx.attrib, "Type") is not None): 
                                id0_ = Utils.getXmlAttrByName(xx.attrib, "Id")[1]
                                val = Utils.getXmlAttrByName(xx.attrib, "Target")[1]
                                typ = Utils.getXmlAttrByName(xx.attrib, "Type")[1]
                                if (typ.endswith("/header")): 
                                    headers.append(val)
                                elif (typ.endswith("/footer")): 
                                    footers.append(val)
                                elif (typ.endswith("/worksheet")): 
                                    sheets[id0_] = val
                                elif (typ.endswith("/image")): 
                                    if (ppt_imgs is not None): 
                                        if (not id0_ in ppt_imgs): 
                                            ppt_imgs[id0_] = val
                                    elif (not id0_ in id_images): 
                                        id_images[id0_] = val
                                elif (typ.endswith("/package")): 
                                    if (not id0_ in id_embeds): 
                                        id_embeds[id0_] = val
                                elif (typ.endswith("/hyperlink")): 
                                    if (not Utils.isNullOrEmpty(val) and not id0_ in self.__m_hyperlinks): 
                                        self.__m_hyperlinks[id0_] = val
            elif (p.is_name("word/numbering.xml")): 
                xml_num = p.get_xml_node(False)
                if (xml_num is not None): 
                    self.__read_number_styles(xml_num)
            elif (p.is_name_starts("ppt/slides/slide") and p.name.endswith(".xml")): 
                xml_doc = p.get_xml_node(False)
                if (xml_doc is None): 
                    continue
                gen = UnitextGen()
                xxx = list()
                xxx.append(xml_doc)
                self._read_node(xxx, gen, None, -1)
                slide = gen.finish(True, None)
                if (slide is None): 
                    continue
                nam = p.name[len("ppt/slides/slide"):]
                ii = nam.find('.')
                if (ii < 0): 
                    continue
                wrapii402 = RefOutArgWrapper(0)
                inoutres403 = Utils.tryParseInt(nam[0:0+ii], wrapii402)
                ii = wrapii402.value
                if (inoutres403): 
                    pass
                else: 
                    ii = (len(ppt_slides) + 1)
                while True: 
                    if (not ii in ppt_slides): 
                        ppt_slides[ii] = slide
                        break
                    ii += 1
        if (xml_odt_content is not None): 
            dh = OdtHelper()
            res = dh.create_uni(xml_odt_content, (None if xml_odt_style is None else xml_odt_style))
            if (res is None): 
                return None
            its = list()
            keys = list()
            res.get_all_items(its, 0)
            for it in its: 
                if ((isinstance(it, UnitextImage)) and it.id0_ is not None and not it.id0_.lower() in keys): 
                    keys.append(it.id0_.lower())
            if (len(its) > 0 and not only_for_pure_text): 
                for o in self.__zip_file.entries: 
                    kkk = o.name.lower()
                    if (not kkk in keys): 
                        continue
                    dat = o.get_data()
                    if (dat is not None and len(dat) > 0): 
                        for it in its: 
                            if ((isinstance(it, UnitextImage)) and it.id0_ is not None and it.id0_.lower() == kkk): 
                                it.content = dat
            return res
        if (len(ppt_slides) > 0): 
            res = UnitextDocument._new404(FileFormat.PPTX, self.__m_data_controls)
            cnt = UnitextContainer()
            res.content = (cnt)
            for kp in ppt_slides.items(): 
                if (len(cnt.children) > 0): 
                    cnt.children.append(UnitextPagebreak())
                cnt.children.append(kp[1])
                if (kp[0] in ppt_images): 
                    imgs = list()
                    kp[1].get_all_items(imgs, 0)
                    for it in imgs: 
                        im = Utils.asObjectOrNull(it, UnitextImage)
                        if (im is not None and Utils.ifNotNull(im.id0_, "") in ppt_images[kp[0]]): 
                            im.id0_ = ppt_images[kp[0]][im.id0_]
                            if (im.id0_.startswith("../")): 
                                im.id0_ = im.id0_[3:]
            if (not only_for_pure_text): 
                ims = list()
                res.get_all_items(ims, 0)
                for p in self.__parts: 
                    kkk = p.name.lower()
                    dat = None
                    for im in ims: 
                        if ((isinstance(im, UnitextImage)) and im.id0_ is not None): 
                            if (kkk.endswith(im.id0_)): 
                                if (dat is None): 
                                    dat = p.get_bytes()
                                im.content = dat
            return res
        if (len(id_embeds) > 0): 
            for p in self.__parts: 
                for kp in id_embeds.items(): 
                    if (not kp[0] in self.__m_embeds): 
                        if (p.name.lower().endswith(kp[1].lower())): 
                            dat = p.get_bytes()
                            if (dat is not None and len(dat) > 0): 
                                doc1 = UnitextService.create_document(p.name, dat, None)
                                if (doc1 is not None and doc1.content is not None): 
                                    self.__m_embeds[kp[0]] = doc1.content
                            break
        if (xml_doc is not None): 
            if (xml_footnotes is not None): 
                li = list()
                li.append(xml_footnotes)
                self.__read_footnotes(li, False)
            if (xml_endnotes is not None): 
                li = list()
                li.append(xml_endnotes)
                self.__read_footnotes(li, True)
            gen = UnitextGen()
            xxx = list()
            xxx.append(xml_doc)
            self._read_node(xxx, gen, None, -1)
            body = gen.finish(True, None)
            if (body is None): 
                return None
            res = UnitextDocument._new404(FileFormat.DOCX, self.__m_data_controls)
            res.content = body
            if (len(headers) > 0 or len(footers) > 0): 
                h = UnitextGen()
                f = UnitextGen()
                for p in self.__parts: 
                    kkk = p.name
                    ii = kkk.find('/')
                    if (ii < 0): 
                        continue
                    kkk = kkk[ii + 1:]
                    if (not kkk in headers and not kkk in footers): 
                        continue
                    xml0_ = p.get_xml_node(False)
                    if (xml0_ is not None): 
                        xxx.clear()
                        xxx.append(xml0_)
                        self._read_node(xxx, (h if kkk in headers else f), None, -1)
                res.header = h.finish(True, None)
                res.footer = f.finish(True, None)
            if (not only_for_pure_text): 
                its = list()
                res.get_all_items(its, 0)
                iii = list()
                iiids = list()
                for i in its: 
                    if ((isinstance(i, UnitextImage)) and i.id0_ is not None and i.id0_ in id_images): 
                        iii.append(Utils.asObjectOrNull(i, UnitextImage))
                        i.tag = (id_images[i.id0_])
                        iiids.append(Utils.asObjectOrNull(i.tag, str))
                if (len(iii) > 0): 
                    for p in self.__parts: 
                        kkk = p.name
                        if (not kkk in iiids): 
                            ii = kkk.find('/')
                            if (ii < 0): 
                                continue
                            kkk = kkk[ii + 1:]
                            if (not kkk in iiids): 
                                continue
                        dat = p.get_bytes()
                        if (dat is not None): 
                            for kp in iii: 
                                if ((Utils.asObjectOrNull(kp.tag, str)) == kkk): 
                                    kp.content = dat
            return res
        if (xml_book is not None and self.__zip_file is not None): 
            res = UnitextDocument._new404(FileFormat.XLSX, self.__m_data_controls)
            books = dict()
            for xml0_ in xml_book: 
                if (Utils.getXmlLocalName(xml0_) == "sheets"): 
                    for xx in xml0_: 
                        id0_ = None
                        nams = None
                        if (xx.attrib is not None): 
                            for a in xx.attrib.items(): 
                                if (Utils.getXmlAttrLocalName(a) == "name"): 
                                    nams = a[1]
                                elif (Utils.getXmlAttrLocalName(a) == "id"): 
                                    id0_ = a[1]
                        if (id0_ is not None and nams is not None and not nams in books): 
                            books[id0_] = nams
            sss = dict()
            for o in self.__zip_file.entries: 
                kkk = o.name
                ii = kkk.find('/')
                if (ii < 0): 
                    continue
                kkk = kkk[ii + 1:]
                id0_ = None
                for kp in sheets.items(): 
                    if (kp[1] == kkk): 
                        id0_ = kp[0]
                        break
                if (id0_ is None): 
                    continue
                sheet_name = None
                wrapsheet_name407 = RefOutArgWrapper(None)
                Utils.tryGetValue(books, id0_, wrapsheet_name407)
                sheet_name = wrapsheet_name407.value
                dat = o.get_data()
                if (dat is None): 
                    continue
                xr = MyXmlReader.create(dat)
                cnt = ExcelHelper.read_sheet(xr, shared_strings, cell_borders, sheet_name)
                if (cnt is None): 
                    continue
                sss[id0_] = cnt
            ss = list()
            for kp in books.items(): 
                if (kp[0] in sss): 
                    if (sss[kp[0]] is not None): 
                        ss.append(sss[kp[0]])
            if (len(ss) == 0): 
                return None
            if (len(ss) == 1): 
                res.content = ss[0]
            else: 
                cnt = UnitextContainer()
                ii = 0
                while ii < len(ss): 
                    if (ii > 0): 
                        cnt.children.append(UnitextPagebreak())
                    cnt.children.append(ss[ii])
                    ii += 1
                res.content = (cnt)
            res._optimize(False, pars)
            return res
        return None
    
    def _read_node(self, stack_nodes : typing.List[xml.etree.ElementTree.Element], gen : 'UnitextGen', style : 'UnitextTextStyle', pict_top : int) -> None:
        if (len(stack_nodes) == 0): 
            return
        node = stack_nodes[len(stack_nodes) - 1]
        for child in node: 
            if (Utils.getXmlLocalName(child) == "Fallback"): 
                stack_nodes.append(child)
                self._read_node(stack_nodes, gen, style, pict_top)
                del stack_nodes[len(stack_nodes) - 1]
                return
        del_text = None
        proof_err = False
        i = 0
        first_pass616 = True
        while True:
            if first_pass616: first_pass616 = False
            else: i += 1
            if (not (i < len(node))): break
            child = node[i]
            locname = Utils.getXmlLocalName(child)
            if (Utils.isNullOrEmpty(locname)): 
                continue
            if (locname == "#text"): 
                continue
            if (proof_err): 
                continue
            swichVal = locname
            if (swichVal == "t"): 
                text = Utils.getXmlInnerText(child)
                if (Utils.isNullOrEmpty(text) or text == del_text): 
                    self.__m_last_char = ' '
                else: 
                    if (del_text is not None): 
                        if (text.startswith(del_text)): 
                            text = text[len(del_text):]
                    if (style is not None and style.upper_case): 
                        text = text.upper()
                    self.__m_last_char = text[len(text) - 1]
                    gen.append_text(text, False)
                del_text = (None)
            elif (swichVal == "sym"): 
                ch = None
                if (child.attrib is not None): 
                    font = None
                    for a in child.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "font"): 
                            font = a[1]
                            break
                    for a in child.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "char"): 
                            nn = 0
                            jj = 0
                            while jj < len(a[1]): 
                                dig = ord(a[1][jj])
                                if (dig >= 0x30 and dig <= 0x39): 
                                    nn = (((nn * 16) + dig) - 0x30)
                                elif (dig >= 0x41 and dig <= 0x46): 
                                    nn = ((((nn * 16) + dig) - 0x41) + 10)
                                elif (dig >= 0x61 and dig <= 0x66): 
                                    nn = ((((nn * 16) + dig) - 0x61) + 10)
                                jj += 1
                            if (a[1][0] == 'F'): 
                                nn -= 0xF000
                            uch = chr(0)
                            if (Utils.compareStrings(Utils.ifNotNull(font, ""), "Symbol", True) == 0): 
                                uch = (chr(nn))
                            else: 
                                uch = WingdingsHelper.get_unicode(nn)
                            if (uch == (chr(0))): 
                                ch = " "
                            else: 
                                ch = "{0}".format(uch)
                if (ch is not None): 
                    gen.append_text(ch, False)
                    self.__m_last_char = ch[0]
            elif (swichVal == "cr"): 
                gen.append_newline(False)
            elif (swichVal == "lastRenderedPageBreak"): 
                gen.append_pagebreak()
            elif (swichVal == "commentRangeStart"): 
                if (child.attrib is not None): 
                    for a in child.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "id"): 
                            cmt = None
                            wrapcmt408 = RefOutArgWrapper(None)
                            inoutres409 = Utils.tryGetValue(self.__m_comments, Utils.ifNotNull(a[1], ""), wrapcmt408)
                            cmt = wrapcmt408.value
                            if (inoutres409): 
                                if (cmt.id0_ is None): 
                                    cmt.id0_ = ("comment" + a[1])
                                gen.append(cmt, None, -1, False)
            elif (swichVal == "commentRangeEnd"): 
                if (child.attrib is not None): 
                    for a in child.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "id"): 
                            cmt = None
                            wrapcmt411 = RefOutArgWrapper(None)
                            inoutres412 = Utils.tryGetValue(self.__m_comments, Utils.ifNotNull(a[1], ""), wrapcmt411)
                            cmt = wrapcmt411.value
                            if (inoutres412): 
                                ecmt = UnitextComment._new410(cmt.id0_ + "_end", cmt.id0_, True)
                                cmt.twin_id = ecmt.id0_
                                ecmt.text = cmt.text
                                ecmt.author = cmt.author
                                gen.append(ecmt, None, -1, False)
                                del self.__m_comments[a[1]]
            elif (swichVal == "br"): 
                val = None
                if (child.attrib is not None and len(child.attrib) > 0 and "type" in Utils.getXmlAttrName(Utils.getXmlAttrByIndex(child.attrib, 0))): 
                    val = Utils.getXmlAttrByIndex(child.attrib, 0)[1]
                if (val == "page"): 
                    gen.append_pagebreak()
                else: 
                    is_new_line = False
                    if (gen.last_not_space_char == ':' or gen.last_not_space_char == '.'): 
                        is_new_line = True
                    if (is_new_line): 
                        gen.append_newline(False)
                    else: 
                        gen.append_newline(False)
            elif (swichVal == "pict"): 
                while True:
                    img1 = None
                    for x in child: 
                        if (Utils.getXmlLocalName(x) == "binData"): 
                            if (img1 is None): 
                                img1 = UnitextImage()
                            try: 
                                img1.content = base64.decodestring((Utils.getXmlInnerText(x)).encode('utf-8', 'ignore'))
                            except Exception as ex: 
                                pass
                            gen.append(img1, None, -1, False)
                        elif (Utils.getXmlLocalName(x) == "shape" and x.attrib is not None): 
                            for a in x.attrib.items(): 
                                if (Utils.getXmlAttrLocalName(a) == "style" and a[1] is not None): 
                                    if (img1 is None): 
                                        img1 = UnitextImage()
                                    DocxToText.__set_image_size(img1, a[1])
                    if (img1 is not None and img1.content is not None): 
                        return
                    gg = UnitextGen()
                    stack_nodes.append(child)
                    self._read_node(stack_nodes, gg, style, pict_top)
                    del stack_nodes[len(stack_nodes) - 1]
                    it = gg.finish(True, None)
                    if (it is None): 
                        break
                    if (isinstance(it, UnitextContainer)): 
                        it.typ = UnitextContainerType.SHAPE
                    else: 
                        cnt = UnitextContainer._new87(UnitextContainerType.SHAPE)
                        cnt.children.append(it)
                        it = cnt._optimize(False, None)
                    if (it is not None): 
                        gen.append(it, None, -1, False)
                    break
            elif (swichVal == "tab"): 
                if (Utils.getXmlLocalName(node) == "tabs"): 
                    pass
                else: 
                    gen.append_text("\t", False)
            elif (swichVal == "p"): 
                num_style = None
                txt_style = None
                for xx in child: 
                    if (Utils.getXmlLocalName(xx) == "pPr"): 
                        id0_ = None
                        lev = 0
                        for xxx in xx: 
                            if (Utils.getXmlLocalName(xxx) == "numPr"): 
                                for chh in xxx: 
                                    if (Utils.getXmlLocalName(chh) == "numId" and chh.attrib is not None and len(chh.attrib) == 1): 
                                        id0_ = Utils.getXmlAttrByIndex(chh.attrib, 0)[1]
                                    elif (Utils.getXmlLocalName(chh) == "ilvl" and chh.attrib is not None and len(chh.attrib) == 1): 
                                        wraplev414 = RefOutArgWrapper(0)
                                        Utils.tryParseInt(Utils.ifNotNull(Utils.getXmlAttrByIndex(chh.attrib, 0)[1], ""), wraplev414)
                                        lev = wraplev414.value
                            elif (Utils.getXmlLocalName(xxx) == "listPr"): 
                                num_style = (DocxToText._read_number_style(xxx))
                                lev = num_style.lvl
                            elif (Utils.getXmlLocalName(xxx) == "pStyle"): 
                                if (xxx.attrib is not None): 
                                    for a in xxx.attrib.items(): 
                                        if (Utils.getXmlAttrLocalName(a) == "val"): 
                                            if (Utils.ifNotNull(a[1], "") in self.__m_text_styles): 
                                                txt_style = self.__m_text_styles[Utils.ifNotNull(a[1], "")]
                                                if (txt_style is not None and txt_style.num_id is not None): 
                                                    if (id0_ is not None or lev > 0): 
                                                        pass
                                                    else: 
                                                        id0_ = txt_style.num_id
                                                        lev = txt_style.num_lvl
                        if (id0_ is not None): 
                            if (id0_ in self.__m_num_styles): 
                                num_style = (self.__m_num_styles[id0_])
                        if (num_style is not None): 
                            gg1 = UnitextGen()
                            stack_nodes.append(child)
                            self._read_node(stack_nodes, gg1, Utils.ifNotNull(txt_style, style), pict_top)
                            del stack_nodes[len(stack_nodes) - 1]
                            gen.append(gg1.finish(True, None), num_style, lev, txt_style is not None and txt_style.is_heading)
                            if (txt_style is not None and txt_style.is_heading): 
                                gen.append_newline(False)
                            break
                if (num_style is None): 
                    stack_nodes.append(child)
                    self._read_node(stack_nodes, gen, Utils.ifNotNull(txt_style, style), pict_top)
                    del stack_nodes[len(stack_nodes) - 1]
                    if (pict_top < 0): 
                        gen.append_newline(False)
                        if (txt_style is not None and txt_style.is_heading): 
                            gen.append_newline(False)
            elif (swichVal == "tbl"): 
                tbl = DocTable()
                stack_nodes.append(child)
                tbl.read(self, stack_nodes)
                del stack_nodes[len(stack_nodes) - 1]
                tab = tbl.create_uni()
                if (tab is not None): 
                    gen.append(tab, None, -1, False)
            elif (swichVal == "fldSimple"): 
                ggg1 = UnitextGen()
                stack_nodes.append(child)
                self._read_node(stack_nodes, ggg1, style, pict_top)
                del stack_nodes[len(stack_nodes) - 1]
                ggt = ggg1.finish(True, None)
                txt = (None if ggt is None else UnitextHelper.get_plaintext(ggt))
                if (not Utils.isNullOrEmpty(txt) and not gen.last_text.endswith(txt)): 
                    gen.append_text(txt, False)
            elif (swichVal == "hyperlink" or swichVal == "hlink"): 
                ok = False
                if (child.attrib is not None): 
                    for a in child.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "id"): 
                            if (a[1] in self.__m_hyperlinks): 
                                ggg = UnitextGen()
                                stack_nodes.append(child)
                                self._read_node(stack_nodes, ggg, style, pict_top)
                                del stack_nodes[len(stack_nodes) - 1]
                                cnt = ggg.finish(True, None)
                                if (cnt is not None): 
                                    if (Utils.ifNotNull(a[1], "") in self.__m_hyperlinks): 
                                        try: 
                                            hr = UnitextHyperlink._new51(str(self.__m_hyperlinks[a[1]]))
                                            hr.children.append(cnt)
                                            gen.append(hr, None, -1, False)
                                        except Exception as xx: 
                                            gen.append(cnt, None, -1, False)
                                    else: 
                                        gen.append(cnt, None, -1, False)
                                    ok = True
                                    break
                        elif (Utils.getXmlAttrLocalName(a) == "dest"): 
                            ggg = UnitextGen()
                            stack_nodes.append(child)
                            self._read_node(stack_nodes, ggg, style, pict_top)
                            del stack_nodes[len(stack_nodes) - 1]
                            cnt = ggg.finish(True, None)
                            if (cnt is not None): 
                                hr = UnitextHyperlink._new51(a[1])
                                hr.children.append(cnt)
                                gen.append(hr, None, -1, False)
                                ok = True
                                break
                if (not ok): 
                    stack_nodes.append(child)
                    self._read_node(stack_nodes, gen, style, pict_top)
                    del stack_nodes[len(stack_nodes) - 1]
            elif (swichVal == "r"): 
                while True:
                    if (child.attrib is not None): 
                        for a in child.attrib.items(): 
                            if (Utils.getXmlAttrLocalName(a) == "rsidRPr"): 
                                if (not Utils.isNullOrEmpty(self.__m_lastrsid) and Utils.compareStrings(a[1], self.__m_lastrsid, True) != 0): 
                                    self.__m_lastrsid = Utils.getXmlAttrLocalName(a)
                                    if ((ord(gen.last_char)) != 0 and not Utils.isWhitespace(gen.last_char)): 
                                        gen.append_text(" ", False)
                    is_sup = -1
                    for rpr in child: 
                        if (Utils.getXmlLocalName(rpr) == "rPr"): 
                            for xxx in rpr: 
                                if (Utils.getXmlLocalName(xxx) == "vertAlign" and xxx.attrib is not None and len(xxx.attrib) > 0): 
                                    if (Utils.getXmlAttrByIndex(xxx.attrib, 0)[1] == "superscript"): 
                                        is_sup = 1
                                    elif (Utils.getXmlAttrByIndex(xxx.attrib, 0)[1] == "subscript"): 
                                        is_sup = 0
                    if (is_sup >= 0): 
                        gg1 = UnitextGen()
                        stack_nodes.append(child)
                        self._read_node(stack_nodes, gg1, style, pict_top)
                        del stack_nodes[len(stack_nodes) - 1]
                        tmp = gg1.finish(True, None)
                        if (tmp is None): 
                            break
                        tt = UnitextHelper.get_plaintext(tmp)
                        if (tt is None): 
                            tt = ""
                        tt = tt.strip()
                        if (tt.startswith("<") and tt.endswith(">")): 
                            tt = tt[1:1+len(tt) - 2]
                        if (len(tt) > 0 and (len(tt) < 10)): 
                            gen.append(UnitextPlaintext._new50(tt, (UnitextPlaintextType.SUB if is_sup == 0 else UnitextPlaintextType.SUP)), None, -1, False)
                            break
                    stack_nodes.append(child)
                    self._read_node(stack_nodes, gen, style, pict_top)
                    del stack_nodes[len(stack_nodes) - 1]
                    break
            elif (swichVal == "footnoteReference"): 
                while True:
                    del_text = (None)
                    if (child.attrib is None): 
                        break
                    for a in child.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "customMarkFollows" and a[1] == "1" and ((i + 1) < len(node))): 
                            ch1 = node[i + 1]
                            if (Utils.getXmlLocalName(ch1) == "t"): 
                                del_text = Utils.getXmlInnerText(ch1)
                                i += 1
                                break
                    for a in child.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "id" and a[1] in self.__m_footnotes): 
                            cnt = self.__m_footnotes[a[1]]
                            if (not Utils.isNullOrEmpty(del_text)): 
                                pl = Utils.asObjectOrNull(cnt, UnitextPlaintext)
                                if (pl is not None and pl.text.startswith(del_text)): 
                                    pl.text = pl.text[len(del_text):].strip()
                            gen.append(UnitextFootnote._new418(cnt, del_text), None, -1, False)
                            break
                    break
            elif (swichVal == "endnoteReference"): 
                if (child.attrib is not None): 
                    for a in child.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "id" and "end" + a[1] in self.__m_footnotes): 
                            gen.append(UnitextFootnote._new257(self.__m_footnotes["end" + a[1]], True), None, -1, False)
                            break
            elif (swichVal == "footnote" or swichVal == "endnote"): 
                while True:
                    gg2 = UnitextGen()
                    stack_nodes.append(child)
                    self._read_node(stack_nodes, gg2, style, pict_top)
                    del stack_nodes[len(stack_nodes) - 1]
                    tmp2 = gg2.finish(True, None)
                    if (tmp2 is None): 
                        break
                    fn = UnitextFootnote._new420(locname == "endnote", tmp2)
                    gen.append(fn, None, -1, False)
                    break
            elif (swichVal == "blip"): 
                if (child.attrib is not None): 
                    for a in child.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "embed"): 
                            img = UnitextImage._new89(a[1])
                            gen.append(img, None, -1, False)
                            for ii in range(len(stack_nodes) - 1, -1, -1):
                                for xxx in stack_nodes[ii]: 
                                    if (Utils.getXmlLocalName(xxx) == "extent" and xxx.attrib is not None): 
                                        xw = 0
                                        yh = 0
                                        for aa in xxx.attrib.items(): 
                                            if (Utils.getXmlAttrLocalName(aa) == "cx"): 
                                                wrapxw422 = RefOutArgWrapper(0)
                                                Utils.tryParseInt(aa[1], wrapxw422)
                                                xw = wrapxw422.value
                                            elif (Utils.getXmlAttrLocalName(aa) == "cy"): 
                                                wrapyh423 = RefOutArgWrapper(0)
                                                Utils.tryParseInt(aa[1], wrapyh423)
                                                yh = wrapyh423.value
                                        if (xw > 0 and yh > 0): 
                                            img.width = "{0}pt".format(math.floor((xw * 72) / 914400))
                                            img.height = "{0}pt".format(math.floor((yh * 72) / 914400))
                            break
            elif (swichVal == "imagedata"): 
                if (child.attrib is not None): 
                    for a in child.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "id"): 
                            img = UnitextImage._new89(a[1])
                            gen.append(img, None, -1, False)
                            if (Utils.getXmlLocalName(node) == "shape" and node.attrib is not None): 
                                for aa in node.attrib.items(): 
                                    if (Utils.getXmlAttrLocalName(aa) == "style"): 
                                        DocxToText.__set_image_size(img, aa[1])
                                        break
                            break
            elif (swichVal == "OLEObject"): 
                if (child.attrib is not None): 
                    for a in child.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "id"): 
                            if (a[1] in self.__m_embeds): 
                                gen.append(self.__m_embeds[a[1]], None, -1, False)
                                break
            elif (swichVal == "sdt"): 
                tag = None
                valu = None
                for x in child: 
                    if (Utils.getXmlLocalName(x) == "sdtPr"): 
                        for xx in x: 
                            if (Utils.getXmlLocalName(xx) == "tag"): 
                                tag = DocxToText.__get_attr_value(xx, "val")
                            elif (Utils.getXmlLocalName(xx) == "date"): 
                                valu = DocxToText.__get_attr_value(xx, "fullDate")
                    elif (Utils.getXmlLocalName(x) == "sdtContent"): 
                        gg3 = UnitextGen()
                        stack_nodes.append(child)
                        self._read_node(stack_nodes, gg3, style, pict_top)
                        del stack_nodes[len(stack_nodes) - 1]
                        tmp3 = gg3.finish(True, None)
                        if (tmp3 is None): 
                            break
                        if (valu is None): 
                            valu = UnitextHelper.get_plaintext(tmp3)
                        if (isinstance(tmp3, UnitextContainer)): 
                            tmp3.typ = UnitextContainerType.CONTENTCONTROL
                        else: 
                            ccc = UnitextContainer._new87(UnitextContainerType.CONTENTCONTROL)
                            ccc.children.append(tmp3)
                            tmp3.parent = (ccc)
                            tmp3 = (ccc)
                        tmp3.html_title = "Content control: {0}".format(tag)
                        tmp3.data = valu
                        tmp3.id0_ = tag
                        gen.append(tmp3, None, -1, False)
                if (tag is not None and valu is not None): 
                    if (not tag in self.__m_data_controls): 
                        self.__m_data_controls[tag] = valu
            elif (swichVal == "ffData"): 
                nam1 = None
                for x in child: 
                    if (Utils.getXmlLocalName(x) == "name"): 
                        nam1 = DocxToText.__get_attr_value(x, "val")
                    elif (Utils.getXmlLocalName(x) == "textInput"): 
                        for xx in x: 
                            if (Utils.getXmlLocalName(xx) == "default"): 
                                val1 = DocxToText.__get_attr_value(xx, "val")
                                if (val1 is not None and nam1 is not None): 
                                    if (not nam1 in self.__m_data_controls): 
                                        self.__m_data_controls[nam1] = val1
            elif (swichVal == "rect"): 
                for a in child.attrib.items(): 
                    if (Utils.getXmlAttrLocalName(a) == "style"): 
                        if (pict_top < 0): 
                            pict_top = 0
                        for s in Utils.splitString(a[1], ';', False): 
                            ii = s.find(':')
                            if (ii <= 0): 
                                continue
                            key = s[0:0+ii].strip().lower()
                            va = s[ii + 1:].strip()
                            if (key == "position"): 
                                if (va != "absolute"): 
                                    break
                            if (key != "top"): 
                                continue
                            for j in range(len(va) - 1, 0, -1):
                                if (str.isdigit(va[j])): 
                                    wrapii426 = RefOutArgWrapper(0)
                                    inoutres427 = Utils.tryParseInt(va[0:0+j + 1], wrapii426)
                                    ii = wrapii426.value
                                    if (not inoutres427): 
                                        break
                                    if (ii > pict_top): 
                                        gen.append_newline(True)
                                        pict_top = ii
                                    break
                            break
                stack_nodes.append(child)
                self._read_node(stack_nodes, gen, style, pict_top)
                del stack_nodes[len(stack_nodes) - 1]
            else: 
                if ((pict_top < 0) and Utils.getXmlLocalName(child) == "txbxContent"): 
                    gen.append_text(" ", False)
                stack_nodes.append(child)
                self._read_node(stack_nodes, gen, style, pict_top)
                del stack_nodes[len(stack_nodes) - 1]
                if ((pict_top < 0) and Utils.getXmlLocalName(child) == "txbxContent"): 
                    gen.append_text(" ", False)
    
    @staticmethod
    def __get_attr_value(n : xml.etree.ElementTree.Element, attr_name : str) -> str:
        if (n.attrib is not None): 
            for a in n.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == attr_name): 
                    return a[1]
        return None
    
    @staticmethod
    def __set_image_size(img : 'UnitextImage', style : str) -> None:
        ii = style.find("width:")
        if (ii >= 0): 
            img.width = style[ii + 6:].strip()
            ii = img.width.find(';')
            if (((ii)) > 0): 
                img.width = img.width[0:0+ii].strip()
        ii = style.find("height:")
        if (ii >= 0): 
            img.height = style[ii + 7:].strip()
            ii = img.height.find(';')
            if (((ii)) > 0): 
                img.height = img.height[0:0+ii].strip()
    
    def __read_footnotes(self, stack_list : typing.List[xml.etree.ElementTree.Element], end : bool) -> None:
        node = stack_list[len(stack_list) - 1]
        for xml0_ in node: 
            if (Utils.getXmlLocalName(xml0_) == "footnote" or Utils.getXmlLocalName(xml0_) == "endnote"): 
                id0_ = None
                if (xml0_.attrib is not None): 
                    for a in xml0_.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "id"): 
                            id0_ = a[1]
                            if (end): 
                                id0_ = ("end" + id0_)
                            break
                if (id0_ is None or id0_ in self.__m_footnotes): 
                    continue
                gen = UnitextGen()
                stack_list.append(xml0_)
                self._read_node(stack_list, gen, None, -1)
                del stack_list[len(stack_list) - 1]
                self.__m_footnotes[id0_] = gen.finish(True, None)
    
    def __read_text_styles(self, node : xml.etree.ElementTree.Element) -> None:
        for xnum in node: 
            if (Utils.getXmlLocalName(xnum) == "style" and xnum.attrib is not None and len(xnum.attrib) >= 1): 
                id0_ = None
                for a in xnum.attrib.items(): 
                    if (Utils.getXmlAttrLocalName(a) == "styleId"): 
                        id0_ = a[1]
                        break
                if (id0_ is None or id0_ in self.__m_text_styles): 
                    continue
                sty = DocxToText.UnitextTextStyle()
                self.__m_text_styles[id0_] = sty
                for x in xnum: 
                    if (Utils.getXmlLocalName(x) == "name"): 
                        if (x.attrib is not None and len(x.attrib) > 0): 
                            sty.name = Utils.getXmlAttrByIndex(x.attrib, 0)[1]
                    elif (Utils.getXmlLocalName(x) == "aliases"): 
                        if (x.attrib is not None and len(x.attrib) > 0): 
                            sty.aliases = Utils.getXmlAttrByIndex(x.attrib, 0)[1]
                    elif (Utils.getXmlLocalName(x) == "basedOn"): 
                        if (x.attrib is not None): 
                            for a in x.attrib.items(): 
                                if (Utils.getXmlAttrLocalName(a) == "val" and a[1] in self.__m_text_styles): 
                                    st0 = self.__m_text_styles[a[1]]
                                    sty.num_id = st0.num_id
                                    sty.num_lvl = st0.num_lvl
                                    sty.upper_case = st0.upper_case
                    elif (Utils.getXmlLocalName(x) == "rPr"): 
                        for xx in x: 
                            if (Utils.getXmlLocalName(xx) == "caps"): 
                                sty.upper_case = True
                    elif (Utils.getXmlLocalName(x) == "pPr"): 
                        for xx in x: 
                            if (Utils.getXmlLocalName(xx) == "numPr"): 
                                for xxx in xx: 
                                    if (Utils.getXmlLocalName(xxx) == "numId" and xxx.attrib is not None): 
                                        for a in xxx.attrib.items(): 
                                            if (Utils.getXmlAttrLocalName(a) == "val"): 
                                                sty.num_id = a[1]
                                    elif (Utils.getXmlLocalName(xxx) == "ilvl" and xxx.attrib is not None): 
                                        for a in xxx.attrib.items(): 
                                            if (Utils.getXmlAttrLocalName(a) == "val"): 
                                                ll = 0
                                                wrapll428 = RefOutArgWrapper(0)
                                                inoutres429 = Utils.tryParseInt(a[1], wrapll428)
                                                ll = wrapll428.value
                                                if (inoutres429): 
                                                    sty.num_lvl = ll
    
    def __read_number_styles(self, node : xml.etree.ElementTree.Element) -> None:
        abstr = dict()
        for xnum in node: 
            if (Utils.getXmlLocalName(xnum) == "abstractNum" and xnum.attrib is not None and len(xnum.attrib) >= 1): 
                id0_ = None
                for a in xnum.attrib.items(): 
                    if (Utils.getXmlAttrLocalName(a) == "abstractNumId"): 
                        id0_ = a[1]
                        break
                if (id0_ is None or id0_ in abstr): 
                    continue
                if (id0_ == "14"): 
                    pass
                nsty = UnitextGenNumStyle._new101(id0_)
                abstr[id0_] = nsty
                for xx in xnum: 
                    if (Utils.getXmlLocalName(xx) == "lvl"): 
                        nlev = UniTextGenNumLevel()
                        nsty.levels.append(nlev)
                        for xxx in xx: 
                            if (xxx.attrib is not None): 
                                if (Utils.getXmlLocalName(xxx) == "numFmt" and len(xxx.attrib) == 1): 
                                    nlev.type0_ = DocxToText._get_num_typ(Utils.getXmlAttrByIndex(xxx.attrib, 0)[1])
                                elif (Utils.getXmlLocalName(xxx) == "lvlText" and len(xxx.attrib) == 1): 
                                    nlev.format0_ = Utils.getXmlAttrByIndex(xxx.attrib, 0)[1]
                                elif (Utils.getXmlLocalName(xxx) == "start" and len(xxx.attrib) == 1): 
                                    ii = 0
                                    wrapii431 = RefOutArgWrapper(0)
                                    inoutres432 = Utils.tryParseInt(Utils.getXmlAttrByIndex(xxx.attrib, 0)[1], wrapii431)
                                    ii = wrapii431.value
                                    if (inoutres432): 
                                        nlev.start = ii
                    elif (Utils.getXmlLocalName(xx) == "numStyleLink" and xx.attrib is not None and len(xx.attrib) > 0): 
                        lid = Utils.getXmlAttrByIndex(xx.attrib, 0)[1]
                        if (lid in abstr): 
                            nsty.levels.extend(abstr[lid].levels)
            elif (Utils.getXmlLocalName(xnum) == "num" and xnum.attrib is not None and len(xnum.attrib) == 1): 
                id0_ = Utils.getXmlAttrByIndex(xnum.attrib, 0)[1]
                int_id = None
                for xx in xnum: 
                    if (Utils.getXmlLocalName(xx) == "abstractNumId" and xx.attrib is not None and len(xx.attrib) == 1): 
                        int_id = Utils.getXmlAttrByIndex(xx.attrib, 0)[1]
                if (int_id is None): 
                    continue
                num0 = None
                wrapnum0438 = RefOutArgWrapper(None)
                inoutres439 = Utils.tryGetValue(abstr, int_id, wrapnum0438)
                num0 = wrapnum0438.value
                if (not inoutres439): 
                    continue
                num = UnitextGenNumStyleEx._new433(num0)
                num.id0_ = id0_
                if (not id0_ in self.__m_num_styles): 
                    self.__m_num_styles[id0_] = num
                for xx in xnum: 
                    if (Utils.getXmlLocalName(xx) == "lvlOverride" and xx.attrib is not None and len(xx.attrib) == 1): 
                        l_ = 0
                        wrapl436 = RefOutArgWrapper(0)
                        inoutres437 = Utils.tryParseInt(Utils.ifNotNull(Utils.getXmlAttrByIndex(xx.attrib, 0)[1], ""), wrapl436)
                        l_ = wrapl436.value
                        if (not inoutres437): 
                            continue
                        if ((l_ < 0) or l_ >= len(num.src.levels)): 
                            continue
                        for xxx in xx: 
                            if (Utils.getXmlLocalName(xxx) == "startOverride" and xxx.attrib is not None): 
                                for a in xxx.attrib.items(): 
                                    if (Utils.getXmlAttrLocalName(a) == "val"): 
                                        s = 0
                                        wraps434 = RefOutArgWrapper(0)
                                        inoutres435 = Utils.tryParseInt(a[1], wraps434)
                                        s = wraps434.value
                                        if (inoutres435): 
                                            if (not l_ in num.override_starts): 
                                                num.override_starts[l_] = s
    
    @staticmethod
    def _read_number_style(xml0_ : xml.etree.ElementTree.Element) -> 'UnitextGenNumStyle':
        res = None
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "ilvl"): 
                res = UnitextGenNumStyle()
                try: 
                    if (x.attrib is not None and len(x.attrib) == 1): 
                        res.lvl = int(Utils.getXmlAttrByIndex(x.attrib, 0)[1])
                except Exception as ee: 
                    pass
            elif (Utils.getXmlLocalName(x) == "ilfo"): 
                if (x.attrib is not None and len(x.attrib) == 1): 
                    if (Utils.getXmlAttrByIndex(x.attrib, 0)[1] == "2"): 
                        res.is_bullet = True
            elif (Utils.getXmlLocalName(x) == "t" and res is not None): 
                if (x.attrib is not None and len(x.attrib) == 1): 
                    res.txt = Utils.getXmlAttrByIndex(x.attrib, 0)[1]
        return res
    
    @staticmethod
    def _get_num_typ(ty : str) -> 'UniTextGenNumType':
        if (ty == "bullet"): 
            return UniTextGenNumType.BULLET
        if ("decimal" in ty): 
            return UniTextGenNumType.DECIMAL
        if (ty == "lowerLetter"): 
            return UniTextGenNumType.LOWERLETTER
        if (ty == "russianLower"): 
            return UniTextGenNumType.LOWERCYRLETTER
        if (ty == "russianUpper"): 
            return UniTextGenNumType.UPPERCYRLETTER
        if (ty == "upperLetter"): 
            return UniTextGenNumType.UPPERLETTER
        if (ty == "lowerRoman"): 
            return UniTextGenNumType.LOWERROMAN
        if ("oman" in ty): 
            return UniTextGenNumType.UPPERROMAN
        return UniTextGenNumType.DECIMAL
    def __enter__(self): return self
    def __exit__(self, typ, val, traceback): self.close()