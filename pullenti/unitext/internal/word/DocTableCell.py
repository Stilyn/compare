# SDK Pullenti Unitext, version 4.3, january 2021. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.unitext.internal.uni.UnitextGen import UnitextGen

class DocTableCell:
    
    def __init__(self) -> None:
        self.grid_num = 0
        self.col_span = 1
        self.row_span = 1
        self.merge_vert = 0
        self.text = None;
        self.uni = None;
    
    def __str__(self) -> str:
        return "N={0}, PS={1}x{2}, V={3} : {4}".format(self.grid_num, self.col_span, self.row_span, self.merge_vert, Utils.ifNotNull(self.text, ""))
    
    def read(self, own : 'DocxToText', stack_nodes : typing.List[xml.etree.ElementTree.Element]) -> None:
        xml0_ = stack_nodes[len(stack_nodes) - 1]
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "tcPr"): 
                for xx in x: 
                    if (Utils.getXmlLocalName(xx) == "gridSpan" and xx.attrib is not None and len(xx.attrib) == 1): 
                        cou = 0
                        wrapcou395 = RefOutArgWrapper(0)
                        inoutres396 = Utils.tryParseInt(Utils.getXmlAttrByIndex(xx.attrib, 0)[1], wrapcou395)
                        cou = wrapcou395.value
                        if (inoutres396): 
                            if (cou > 1): 
                                self.col_span = cou
                    elif (Utils.getXmlLocalName(xx) == "vMerge"): 
                        self.merge_vert = 1
                        if (len(xx.attrib) > 0 and xx.attrib is not None and Utils.getXmlAttrByIndex(xx.attrib, 0)[1] == "restart"): 
                            self.merge_vert = 2
        gen = UnitextGen()
        stack_nodes.append(xml0_)
        own._read_node(stack_nodes, gen, None, -1)
        del stack_nodes[len(stack_nodes) - 1]
        self.uni = gen.finish(True, None)