# SDK Pullenti Unitext, version 4.3, january 2021. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.UnitextContainerType import UnitextContainerType
from pullenti.unitext.UnitextContainer import UnitextContainer

class UnitextHyperlink(UnitextContainer):
    """ Гиперссылка """
    
    def __init__(self) -> None:
        super().__init__()
        self.href = None;
        self.is_internal = False
        self.typ = UnitextContainerType.URL
    
    def __str__(self) -> str:
        return "Hyperlink {0}".format(Utils.ifNotNull(self.href, ""))
    
    def clone(self) -> 'UnitextItem':
        res = UnitextHyperlink()
        res._clone_from2(self)
        res.href = self.href
        res.is_internal = self.is_internal
        return res
    
    @property
    def _inner_tag(self) -> str:
        return "hyplnk"
    
    def get_plaintext(self, res : io.StringIO, pars : 'GetPlaintextParam') -> None:
        if (pars is not None and pars.set_positions): 
            self.begin_char = res.tell()
        super().get_plaintext(res, pars)
        if (pars is None): 
            pars = UnitextItem._m_def_params
        if (not Utils.isNullOrEmpty(pars.hyperlinks_template) and self.href is not None and not self.is_internal): 
            tmp = io.StringIO()
            i = self.begin_char
            while i < res.tell(): 
                print(Utils.getCharAtStringIO(res, i), end="", file=tmp)
                i += 1
            txt = Utils.toStringStringIO(tmp)
            if (tmp.tell() == 0): 
                print(self.href, end="", file=res)
            elif (Utils.compareStrings(self.href, txt, True) != 0): 
                print(pars.hyperlinks_template.replace("%1", self.href), end="", file=res)
        if (pars is not None and pars.set_positions): 
            self.end_char = (res.tell() - 1)
    
    def get_html(self, res : io.StringIO, par : 'GetHtmlParam') -> None:
        if (not par.call_before(self, res)): 
            return
        tit = self.href
        if (self.html_title is not None): 
            tmp = io.StringIO()
            MiscHelper.correct_html_value(tmp, self.html_title, True, False)
            tit = Utils.toStringStringIO(tmp)
        if (self.html_style is not None): 
            print("<span style=\"{0}\">".format(self.html_style), end="", file=res, flush=True)
        if (self.is_internal): 
            print("<i>", end="", file=res)
        if (self.href is not None): 
            print("<a href=\"{0}\" title=\"{1}\"{2}".format(self.href, Utils.ifNotNull(tit, ""), (" target=\"_blank\"" if par.hyperlinks_target_blank or self.href.startswith("http") else "")), end="", file=res, flush=True)
        else: 
            print("<span style=\"text-decoration:underline\" title=\"{0}\"".format(Utils.ifNotNull(tit, "")), end="", file=res, flush=True)
        if (self.id0_ is not None): 
            print(" id=\"{0}\"".format(self.id0_), end="", file=res, flush=True)
        print(">", end="", file=res)
        for ch in self.children: 
            ch.get_html(res, par)
        if (self.href is not None): 
            print("</a>", end="", file=res)
        else: 
            print("</span>", end="", file=res)
        if (self.is_internal): 
            print("</i>", end="", file=res)
        if (self.html_style is not None): 
            print("</span>", end="", file=res)
        par.call_after(self, res)
    
    def get_xml(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("hyperlink")
        self._write_xml_attrs(xml0_)
        if (self.href is not None): 
            xml0_.write_attribute_string("href", MiscHelper.correct_xml_value(self.href))
            if (self.is_internal): 
                xml0_.write_attribute_string("internal", "true")
        for ch in self.children: 
            ch.get_xml(xml0_)
        xml0_.write_end_element()
    
    def from_xml(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        super().from_xml(xml0_)
        if (xml0_.attrib is not None): 
            for a in xml0_.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == "href"): 
                    self.href = a[1]
                elif (Utils.getXmlAttrLocalName(a) == "internal"): 
                    self.is_internal = a[1] == "true"
    
    @staticmethod
    def _new51(_arg1 : str) -> 'UnitextHyperlink':
        res = UnitextHyperlink()
        res.href = _arg1
        return res