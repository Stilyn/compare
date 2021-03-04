# SDK Pullenti Unitext, version 4.3, january 2021. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.unitext.internal.uni.UniTextGenNumType import UniTextGenNumType
from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.UnitextContainer import UnitextContainer
from pullenti.unitext.UnitextList import UnitextList
from pullenti.unitext.UnitextListitem import UnitextListitem
from pullenti.unitext.UnitextPlaintextType import UnitextPlaintextType
from pullenti.unitext.UnitextPlaintext import UnitextPlaintext
from pullenti.unitext.UnitextNewline import UnitextNewline
from pullenti.unitext.UnitextFootnote import UnitextFootnote
from pullenti.unitext.UnitextPagebreak import UnitextPagebreak

class UnitextGen:
    
    def __init__(self) -> None:
        self.__m_text = io.StringIO()
        self.__m_res = UnitextContainer()
        self.__m_new_res = False
        self.__m_stack = list()
        self.last_not_space_char = chr(0)
        self.last_char = chr(0)
    
    def clear_all(self) -> None:
        Utils.setLengthStringIO(self.__m_text, 0)
        self.__m_stack.clear()
        if (self.__m_new_res): 
            self.__m_res = UnitextContainer()
        else: 
            self.__m_res.children.clear()
    
    def finish(self, is_content : bool, pars : 'CreateDocumentParam'=None) -> 'UnitextItem':
        self.__flush_text()
        res = self.__m_res._optimize(is_content, pars)
        self.__m_new_res = res == self.__m_res
        return res
    
    @property
    def last_text(self) -> str:
        return Utils.toStringStringIO(self.__m_text)
    
    def __flush_text(self) -> None:
        if (self.__m_text.tell() > 0): 
            t = UnitextPlaintext._new49(Utils.toStringStringIO(self.__m_text))
            Utils.setLengthStringIO(self.__m_text, 0)
            self.append(t, None, -1, False)
    
    def append_newline(self, if_not_prev_newline : bool=False) -> None:
        if (if_not_prev_newline): 
            if (len(self.__m_res.children) > 0 and self.__m_text.tell() == 0): 
                if (isinstance(self.__m_res.children[len(self.__m_res.children) - 1], UnitextNewline)): 
                    return
        self.append(UnitextNewline(), None, -1, False)
        self.last_char = '\r'
    
    def append_pagebreak(self) -> None:
        self.append(UnitextPagebreak(), None, -1, False)
        self.last_char = '\f'
    
    def append(self, blk : 'UnitextItem', num_styl : 'IUnitextGenNumStyle'=None, num_level : int=-1, do_num_style_as_text : bool=False) -> None:
        self.__flush_text()
        if (num_styl is not None and num_styl.txt is not None): 
            list0 = self.append_list_item(blk, num_styl.txt, None, num_styl.lvl, num_styl)
            return
        if (num_styl is None or (num_level < 0)): 
            if (blk is not None): 
                if ((isinstance(blk, UnitextFootnote)) and len(self.__m_res.children) > 0): 
                    txt = Utils.asObjectOrNull(self.__m_res.children[len(self.__m_res.children) - 1], UnitextPlaintext)
                    if (txt is not None and txt.typ == UnitextPlaintextType.SUP): 
                        if (txt.text == blk.custom_mark): 
                            del self.__m_res.children[len(self.__m_res.children) - 1]
                if (num_styl is not None): 
                    self.append_newline(True)
                self.__m_res.children.append(blk)
                if (num_styl is not None): 
                    self.append_newline(False)
            return
        num = num_styl.process(num_level)
        if (num is None): 
            if (blk is not None): 
                self.__m_res.children.append(blk)
            return
        if (do_num_style_as_text): 
            self.append_newline(True)
            self.__m_res.children.append(UnitextPlaintext._new49(num + " "))
            if (blk is not None): 
                self.__m_res.children.append(blk)
            self.append_newline(False)
            return
        numlev = num_styl.get_level(num_level)
        list0_ = self.append_list_item(blk, num, num_styl.id0_, num_level, None)
        if (list0_ is not None and numlev.type0_ == UniTextGenNumType.BULLET): 
            list0_.unorder_prefix = (Utils.ifNotNull(numlev.format0_, ""))
    
    def append_list_item(self, content : 'UnitextItem', pref : str, num_style_id : str, num_level : int, num_styl : 'IUnitextGenNumStyle'=None) -> 'UnitextList':
        self.__flush_text()
        list0_ = None
        for i in range(len(self.__m_res.children) - 1, -1, -1):
            if (isinstance(self.__m_res.children[i], UnitextNewline)): 
                pass
            else: 
                list0_ = (Utils.asObjectOrNull(self.__m_res.children[i], UnitextList))
                break
        if (list0_ is not None and (((Utils.asObjectOrNull(list0_.tag, str)) == num_style_id or num_style_id is None))): 
            if (num_style_id is None and num_styl is None): 
                num_style_id = (Utils.asObjectOrNull(list0_.tag, str))
                num_level = -1
            while True:
                if (list0_.level == num_level): 
                    it0 = UnitextListitem._new336(content)
                    if (pref is not None): 
                        it0.prefix = (UnitextPlaintext._new49(pref))
                    list0_.items.append(it0)
                    return list0_
                if ((num_level < 0) or (list0_.level < num_level)): 
                    if (len(list0_.items) == 0): 
                        break
                    last = list0_.items[len(list0_.items) - 1]
                    if (last.sublist is not None): 
                        list0_ = last.sublist
                        continue
                    if (num_level < 0): 
                        num_level = list0_.level
                        continue
                    if (list0_.level < (num_level - 1)): 
                        break
                    last.sublist = UnitextList._new338(num_level, num_style_id)
                    list0_ = last.sublist
                    continue
                break
        if (num_level < 0): 
            num_level = 0
        list0_ = UnitextList._new338(num_level, num_style_id)
        if (num_styl is not None and num_styl.is_bullet): 
            list0_.unorder_prefix = num_styl.txt
        self.__m_res.children.append(list0_)
        self.__m_res.children.append(UnitextNewline())
        it = UnitextListitem._new336(content)
        if (pref is not None and list0_.unorder_prefix is None): 
            it.prefix = (UnitextPlaintext._new49(pref))
        list0_.items.append(it)
        return list0_
    
    def append_text(self, txt : str, check_table : bool=False) -> None:
        in_table_lev = 0
        i = 0
        first_pass609 = True
        while True:
            if first_pass609: first_pass609 = False
            else: i += 1
            if (not (i < len(txt))): break
            ch = txt[i]
            self.last_char = ch
            if ((ord(ch)) == 0xD or (ord(ch)) == 0xA): 
                if ((ord(ch)) == 0xD and ((i + 1) < len(txt)) and (ord(txt[i + 1])) == 0xA): 
                    i += 1
                self.append_newline(False)
                continue
            if (ch == '\f' and in_table_lev == 0): 
                self.append_pagebreak()
                continue
            if ((ord(ch)) == 0x1E and check_table): 
                in_table_lev += 1
            if ((ord(ch)) == 0x1F and check_table): 
                in_table_lev -= 1
            if ((ord(ch)) == 0xAD): 
                continue
            if (((ord(ch)) != 9 and (ord(ch)) != 7 and ch != '\f') and ((ord(ch)) < 0x1E)): 
                ch = ' '
            print(ch, end="", file=self.__m_text)
            if (not Utils.isWhitespace(ch)): 
                self.last_not_space_char = ch
    
    @staticmethod
    def _convert_to_pt(val : str, det_typ : str=None) -> str:
        vv = UnitextGen._convert_tomm(val, det_typ)
        if (vv == 0): 
            return val
        else: 
            return "{0}pt".format(vv)
    
    @staticmethod
    def _convert_tomm(val : str, det_typ : str=None) -> int:
        if (val is None): 
            return 0
        f = 0
        i = 0
        typ = None
        i = 0
        while i < len(val): 
            if (str.isalpha(val[i]) or val[i] == ';'): 
                typ = val[i:].lower()
                val = val[0:0+i]
                break
            i += 1
        if (Utils.isNullOrEmpty(typ)): 
            typ = det_typ
        if (Utils.isNullOrEmpty(typ)): 
            return math.floor(f)
        wrapf342 = RefOutArgWrapper(0)
        inoutres343 = MiscHelper.try_parse_float(val, wrapf342)
        f = wrapf342.value
        if (inoutres343): 
            pass
        else: 
            return 0
        if (typ.startswith("pt")): 
            pass
        elif (typ.startswith("pc")): 
            f = ((f * (72)) / (6))
        elif (typ.startswith("cm")): 
            f = ((f * (72)) / 2.54)
        elif (typ.startswith("mm")): 
            f = ((f * (72)) / 25.4)
        elif (typ.startswith("px")): 
            f = (f * 0.75)
        elif (typ.startswith("in")): 
            f = (f * 72)
        else: 
            return 0
        return math.floor(f)