# SDK Pullenti Lingvo, version 4.3, january 2021.
# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import operator
import datetime
import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.date.DatePointerType import DatePointerType
from pullenti.ner.date.internal.DateExToken import DateExToken
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.Referent import Referent
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.date.DateRangeReferent import DateRangeReferent

class DateRelHelper:
    
    @staticmethod
    def create_referents(et : 'DateExToken') -> typing.List['ReferentToken']:
        if (not et.is_diap or len(et.items_to) == 0): 
            li = DateRelHelper.__create_refs(et.items_from)
            if (li is None or len(li) == 0): 
                return None
            return li
        li_fr = DateRelHelper.__create_refs(et.items_from)
        li_to = DateRelHelper.__create_refs(et.items_to)
        ra = DateRangeReferent()
        if (len(li_fr) > 0): 
            ra.date_from = Utils.asObjectOrNull(li_fr[0].tag, DateReferent)
        if (len(li_to) > 0): 
            ra.date_to = Utils.asObjectOrNull(li_to[0].tag, DateReferent)
        res = list()
        res.extend(li_fr)
        res.extend(li_to)
        res.append(ReferentToken(ra, et.begin_token, et.end_token))
        if (len(res) == 0): 
            return None
        res[0].tag = (ra)
        return res
    
    @staticmethod
    def __create_refs(its : typing.List['DateExItemToken']) -> typing.List['ReferentToken']:
        res = list()
        own = None
        i = 0
        first_pass3081 = True
        while True:
            if first_pass3081: first_pass3081 = False
            else: i += 1
            if (not (i < len(its))): break
            it = its[i]
            d = DateReferent()
            if (it.is_value_relate): 
                d.is_relative = True
            if (own is not None): 
                d.higher = own
            if (it.typ == DateExToken.DateExItemTokenType.DAY): 
                d.day = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.DAYOFWEEK): 
                d.day_of_week = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.HOUR): 
                d.hour = it.value
                if (((i + 1) < len(its)) and its[i + 1].typ == DateExToken.DateExItemTokenType.MINUTE and not its[i + 1].is_value_relate): 
                    d.minute = its[i + 1].value
                    i += 1
            elif (it.typ == DateExToken.DateExItemTokenType.MINUTE): 
                d.minute = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.MONTH): 
                d.month = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.QUARTAL): 
                d.quartal = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.WEEK): 
                d.week = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.YEAR): 
                d.year = it.value
            else: 
                continue
            res.append(ReferentToken(d, it.begin_token, it.end_token))
            own = d
            it.src = d
        if (len(res) > 0): 
            res[0].tag = (own)
        return res
    
    @staticmethod
    def __create_date_ex(dr : 'DateReferent') -> typing.List['DateExItemToken']:
        res = list()
        while dr is not None: 
            n = 0
            for s in dr.slots: 
                it = DateExToken.DateExItemToken._new678(None, None, DateExToken.DateExItemTokenType.UNDEFINED)
                if (dr.get_string_value(DateReferent.ATTR_ISRELATIVE) == "true"): 
                    it.is_value_relate = True
                if (s.type_name == DateReferent.ATTR_YEAR): 
                    it.typ = DateExToken.DateExItemTokenType.YEAR
                    wrapn679 = RefOutArgWrapper(0)
                    inoutres680 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn679)
                    n = wrapn679.value
                    if (inoutres680): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_QUARTAL): 
                    it.typ = DateExToken.DateExItemTokenType.QUARTAL
                    wrapn681 = RefOutArgWrapper(0)
                    inoutres682 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn681)
                    n = wrapn681.value
                    if (inoutres682): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_MONTH): 
                    it.typ = DateExToken.DateExItemTokenType.MONTH
                    wrapn683 = RefOutArgWrapper(0)
                    inoutres684 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn683)
                    n = wrapn683.value
                    if (inoutres684): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_WEEK): 
                    it.typ = DateExToken.DateExItemTokenType.WEEK
                    wrapn685 = RefOutArgWrapper(0)
                    inoutres686 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn685)
                    n = wrapn685.value
                    if (inoutres686): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_DAYOFWEEK): 
                    it.typ = DateExToken.DateExItemTokenType.DAYOFWEEK
                    wrapn687 = RefOutArgWrapper(0)
                    inoutres688 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn687)
                    n = wrapn687.value
                    if (inoutres688): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_DAY): 
                    it.typ = DateExToken.DateExItemTokenType.DAY
                    wrapn689 = RefOutArgWrapper(0)
                    inoutres690 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn689)
                    n = wrapn689.value
                    if (inoutres690): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_HOUR): 
                    it.typ = DateExToken.DateExItemTokenType.HOUR
                    wrapn691 = RefOutArgWrapper(0)
                    inoutres692 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn691)
                    n = wrapn691.value
                    if (inoutres692): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_MINUTE): 
                    it.typ = DateExToken.DateExItemTokenType.MINUTE
                    wrapn693 = RefOutArgWrapper(0)
                    inoutres694 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn693)
                    n = wrapn693.value
                    if (inoutres694): 
                        it.value = n
                if (it.typ != DateExToken.DateExItemTokenType.UNDEFINED): 
                    res.insert(0, it)
            dr = dr.higher
        res.sort(key=operator.attrgetter('typ'))
        return res
    
    @staticmethod
    def calculate_date(dr : 'DateReferent', now : datetime.datetime, tense : int) -> datetime.datetime:
        if (dr.pointer == DatePointerType.TODAY): 
            return now
        if (not dr.is_relative and dr.dt is not None): 
            return dr.dt
        det = DateExToken(None, None)
        det.items_from = DateRelHelper.__create_date_ex(dr)
        return det.get_date(now, tense)
    
    @staticmethod
    def calculate_date_range(dr : 'DateReferent', now : datetime.datetime, from0_ : datetime.datetime, to : datetime.datetime, tense : int) -> bool:
        if (dr.pointer == DatePointerType.TODAY): 
            from0_.value = now
            to.value = now
            return True
        if (not dr.is_relative and dr.dt is not None): 
            to.value = dr.dt
            from0_.value = to.value
            return True
        det = DateExToken(None, None)
        det.items_from = DateRelHelper.__create_date_ex(dr)
        inoutres695 = det.get_dates(now, from0_, to, tense)
        return inoutres695
    
    @staticmethod
    def calculate_date_range2(dr : 'DateRangeReferent', now : datetime.datetime, from0_ : datetime.datetime, to : datetime.datetime, tense : int) -> bool:
        from0_.value = datetime.datetime.min
        to.value = datetime.datetime.max
        dt0 = None
        dt1 = None
        if (dr.date_from is None): 
            if (dr.date_to is None): 
                return False
            wrapdt0696 = RefOutArgWrapper(None)
            wrapdt1697 = RefOutArgWrapper(None)
            inoutres698 = DateRelHelper.calculate_date_range(dr.date_to, now, wrapdt0696, wrapdt1697, tense)
            dt0 = wrapdt0696.value
            dt1 = wrapdt1697.value
            if (not inoutres698): 
                return False
            to.value = dt1
            return True
        elif (dr.date_to is None): 
            wrapdt0699 = RefOutArgWrapper(None)
            wrapdt1700 = RefOutArgWrapper(None)
            inoutres701 = DateRelHelper.calculate_date_range(dr.date_from, now, wrapdt0699, wrapdt1700, tense)
            dt0 = wrapdt0699.value
            dt1 = wrapdt1700.value
            if (not inoutres701): 
                return False
            from0_.value = dt0
            return True
        wrapdt0705 = RefOutArgWrapper(None)
        wrapdt1706 = RefOutArgWrapper(None)
        inoutres707 = DateRelHelper.calculate_date_range(dr.date_from, now, wrapdt0705, wrapdt1706, tense)
        dt0 = wrapdt0705.value
        dt1 = wrapdt1706.value
        if (not inoutres707): 
            return False
        from0_.value = dt0
        dt2 = None
        dt3 = None
        wrapdt2702 = RefOutArgWrapper(None)
        wrapdt3703 = RefOutArgWrapper(None)
        inoutres704 = DateRelHelper.calculate_date_range(dr.date_to, now, wrapdt2702, wrapdt3703, tense)
        dt2 = wrapdt2702.value
        dt3 = wrapdt3703.value
        if (not inoutres704): 
            return False
        to.value = dt3
        return True
    
    @staticmethod
    def append_to_string(dr : 'DateReferent', res : io.StringIO) -> None:
        dt0 = None
        dt1 = None
        cur = (datetime.datetime.now() if ProcessorService.DEBUG_CURRENT_DATE_TIME is None else ProcessorService.DEBUG_CURRENT_DATE_TIME)
        wrapdt0708 = RefOutArgWrapper(None)
        wrapdt1709 = RefOutArgWrapper(None)
        inoutres710 = DateRelHelper.calculate_date_range(dr, cur, wrapdt0708, wrapdt1709, 0)
        dt0 = wrapdt0708.value
        dt1 = wrapdt1709.value
        if (not inoutres710): 
            return
        DateRelHelper.__append_dates(cur, dt0, dt1, res)
    
    @staticmethod
    def append_to_string2(dr : 'DateRangeReferent', res : io.StringIO) -> None:
        dt0 = None
        dt1 = None
        cur = (datetime.datetime.now() if ProcessorService.DEBUG_CURRENT_DATE_TIME is None else ProcessorService.DEBUG_CURRENT_DATE_TIME)
        wrapdt0711 = RefOutArgWrapper(None)
        wrapdt1712 = RefOutArgWrapper(None)
        inoutres713 = DateRelHelper.calculate_date_range2(dr, cur, wrapdt0711, wrapdt1712, 0)
        dt0 = wrapdt0711.value
        dt1 = wrapdt1712.value
        if (not inoutres713): 
            return
        DateRelHelper.__append_dates(cur, dt0, dt1, res)
    
    @staticmethod
    def __append_dates(cur : datetime.datetime, dt0 : datetime.datetime, dt1 : datetime.datetime, res : io.StringIO) -> None:
        mon0 = dt0.month
        print(" ({0}.{1}.{2}".format(dt0.year, "{:02d}".format(mon0), "{:02d}".format(dt0.day)), end="", file=res, flush=True)
        if (dt0.hour > 0 or dt0.minute > 0): 
            print(" {0}:{1}".format("{:02d}".format(dt0.hour), "{:02d}".format(dt0.minute)), end="", file=res, flush=True)
        if (dt0 != dt1): 
            mon1 = dt1.month
            print("-{0}.{1}.{2}".format(dt1.year, "{:02d}".format(mon1), "{:02d}".format(dt1.day)), end="", file=res, flush=True)
            if (dt1.hour > 0 or dt1.minute > 0): 
                print(" {0}:{1}".format("{:02d}".format(dt1.hour), "{:02d}".format(dt1.minute)), end="", file=res, flush=True)
        monc = cur.month
        print(" отн. {0}.{1}.{2}".format(cur.year, "{:02d}".format(monc), "{:02d}".format(cur.day)), end="", file=res, flush=True)
        if (cur.hour > 0 or cur.minute > 0): 
            print(" {0}:{1}".format("{:02d}".format(cur.hour), "{:02d}".format(cur.minute)), end="", file=res, flush=True)
        print(")", end="", file=res)