# SDK Pullenti Unitext, version 4.3, january 2021. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import gzip
import zlib
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import Stream

class ArchiveHelper:
    """ Работа с архивами и сжатием """
    
    @staticmethod
    def compress_gzip(dat : bytearray) -> bytearray:
        """ Заархивировать массив байт алгоритмом GZip
        
        Args:
            dat(bytearray): исходный массив
        
        Returns:
            bytearray: заархивированый массив
        """
        with MemoryStream() as res: 
            with MemoryStream(dat) as input0_: 
                input0_.position = 0
                with Stream(gzip.GzipFile(fileobj=res.getstream(), mode='w')) as deflate: 
                    input0_.writeto(deflate)
                    deflate.flush()
                    deflate.close()
            return res.toarray()
    
    @staticmethod
    def decompress_gzip(zip0_ : bytearray) -> bytearray:
        """ Разархивировать байтовый массив алгоритмом GZip
        
        Args:
            zip0_(bytearray): архивированный массив
        
        Returns:
            bytearray: результат
        """
        with MemoryStream(zip0_) as data: 
            data.position = 0
            with MemoryStream() as unzip: 
                buf = Utils.newArrayOfBytes(len(zip0_) + len(zip0_), 0)
                with Stream(gzip.GzipFile(fileobj=data.getstream(), mode='r')) as deflate: 
                    while True:
                        i = -1
                        try: 
                            ii = 0
                            while ii < len(buf): 
                                buf[ii] = (0)
                                ii += 1
                            i = deflate.read(buf, 0, len(buf))
                        except Exception as ex: 
                            for i in range(len(buf) - 1, -1, -1):
                                if (buf[i] != (0)): 
                                    unzip.write(buf, 0, i + 1)
                                    break
                            else: i = -1
                            break
                        if (i < 1): 
                            break
                        unzip.write(buf, 0, i)
                res = unzip.toarray()
                return res
    
    @staticmethod
    def compress_zlib(dat : bytearray) -> bytearray:
        """ Заархивировать байтовый массив алгоритмом Zlib
        
        Args:
            dat(bytearray): исходный массив
        
        Returns:
            bytearray: заархивированый массив
        """
        return zlib.compress(dat)
    
    @staticmethod
    def decompress_zlib(zip0_ : bytearray) -> bytearray:
        """ Разархивировать байтовый массив алгоритмом Zlib.
        
        Args:
            zip0_(bytearray): архивированный массив
        
        Returns:
            bytearray: результат
        """
        if (zip0_ is None or (len(zip0_) < 4)): 
            return None
        return zlib.decompress(zip0_)
    
    @staticmethod
    def compress_deflate(dat : bytearray) -> bytearray:
        """ Заархивировать байтовый массив алгоритмом Deflate (без Zlib-заголовка)
        
        Args:
            dat(bytearray): исходный массив
        
        Returns:
            bytearray: заархивированый массив
        """
        zip0_ = None
        zip0_ = zlib.compress(dat, -15)
        return zip0_
    
    @staticmethod
    def decompress_deflate(zip0_ : bytearray) -> bytearray:
        """ Разархивировать байтовый массив алгоритмом Deflate (без Zlib-заголовка)
        
        Args:
            zip0_(bytearray): архивированный массив
        
        Returns:
            bytearray: результат
        """
        if (zip0_ is None or (len(zip0_) < 1)): 
            return None
        return zlib.decompress(zip0_, -15)