# SDK Pullenti Unitext, version 4.3, january 2021. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import math
import base64
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Xml import XmlWriter

from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.UnilayOcrQuality import UnilayOcrQuality

class UnilayRectangle:
    """ Прямоугольник тексто-графического слоя """
    
    def __init__(self) -> None:
        self.page = None;
        self.left = 0
        self.top = 0
        self.right = 0
        self.bottom = 0
        self.text = None;
        self.image_content = None;
        self.ignored = False
        self.line_number = 0
        self.quality = UnilayOcrQuality.UNDEFINED
        self.tag = None;
    
    def __str__(self) -> str:
        res = "{0}..{1} x {2}..{3}".format(round(self.left, 2), round(self.right, 2), round(self.top, 2), round(self.bottom, 2))
        if (self.text is not None): 
            return "{0}: {1}".format(res, self.text)
        if (self.image_content is not None): 
            return "{0}: Image".format(res)
        return res
    
    def get_xml(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("rect")
        if (self.line_number > 0): 
            xml0_.write_attribute_string("line", str(self.line_number))
        xml0_.write_attribute_string("left", MiscHelper.out_double(self.left))
        xml0_.write_attribute_string("top", MiscHelper.out_double(self.top))
        xml0_.write_attribute_string("right", MiscHelper.out_double(self.right))
        xml0_.write_attribute_string("bottom", MiscHelper.out_double(self.bottom))
        if (self.quality != UnilayOcrQuality.UNDEFINED): 
            xml0_.write_attribute_string("q", Utils.enumToString(self.quality).lower())
        if (self.image_content is not None): 
            xml0_.write_element_string("image", base64.encodestring(self.image_content).decode('utf-8', 'ignore'))
        elif (self.text is not None): 
            xml0_.write_element_string("text", Utils.ifNotNull(MiscHelper.correct_xml_value(self.text), ""))
        xml0_.write_end_element()
    
    def restore(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        d = 0
        if (xml0_.attrib is not None): 
            for a in xml0_.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == "line"): 
                    i = 0
                    wrapi480 = RefOutArgWrapper(0)
                    inoutres481 = Utils.tryParseInt(a[1], wrapi480)
                    i = wrapi480.value
                    if (inoutres481): 
                        self.line_number = i
                elif (Utils.getXmlAttrLocalName(a) == "left"): 
                    wrapd482 = RefOutArgWrapper(0)
                    inoutres483 = MiscHelper.try_parse_double(a[1], wrapd482)
                    d = wrapd482.value
                    if (inoutres483): 
                        self.left = d
                elif (Utils.getXmlAttrLocalName(a) == "top"): 
                    wrapd484 = RefOutArgWrapper(0)
                    inoutres485 = MiscHelper.try_parse_double(a[1], wrapd484)
                    d = wrapd484.value
                    if (inoutres485): 
                        self.top = d
                elif (Utils.getXmlAttrLocalName(a) == "right"): 
                    wrapd486 = RefOutArgWrapper(0)
                    inoutres487 = MiscHelper.try_parse_double(a[1], wrapd486)
                    d = wrapd486.value
                    if (inoutres487): 
                        self.right = d
                elif (Utils.getXmlAttrLocalName(a) == "bottom"): 
                    wrapd488 = RefOutArgWrapper(0)
                    inoutres489 = MiscHelper.try_parse_double(a[1], wrapd488)
                    d = wrapd488.value
                    if (inoutres489): 
                        self.bottom = d
                elif (Utils.getXmlAttrLocalName(a) == "q"): 
                    try: 
                        self.quality = (Utils.valToEnum(a[1], UnilayOcrQuality))
                    except Exception as ex490: 
                        pass
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "text"): 
                self.text = Utils.getXmlInnerText(x)
            elif (Utils.getXmlLocalName(x) == "image"): 
                self.image_content = base64.decodestring((Utils.getXmlInnerText(x)).encode('utf-8', 'ignore'))
    
    @staticmethod
    def _new479(_arg1 : 'UnilayPage') -> 'UnilayRectangle':
        res = UnilayRectangle()
        res.page = _arg1
        return res