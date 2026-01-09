[START OUTPUT}

#!/usr/bin/env python3  
# -*- coding: utf-8 -*-  
"""  
🌍 GEO-PROXY MASTER v6.0.0 - Enterprise Proxy Orchestration System  
⚡ نظام بروكسي جغرافي متقدم مع تجنب الكشف والحظر  
🔒 مستوى المؤسسة مع طبقات متعددة من التمويه والمرونة  
"""  
  
import asyncio  
import aiohttp  
import random  
import time  
import logging  
import json  
import re  
import hashlib  
import string  
import socket  
import struct  
import ipaddress  
from datetime import datetime, timedelta  
from typing import List, Dict, Optional, Tuple, Set, Any, Callable  
from dataclasses import dataclass, field  
from enum import Enum, auto  
from collections import defaultdict, deque  
from concurrent.futures import ThreadPoolExecutor  
import pickle  
import base64  
import ssl  
import certifi  
from urllib.parse import urlparse  
import dns.asyncresolver  
import asyncio  
from asyncio import Semaphore, Queue, Lock  
import aiofiles  
import zlib  
import uuid  
  
# ========== ADVANCED CONFIGURATION ==========  
class __ᴄᴏɴғɪɢ:  
    """تهيئة متقدمة مع تسميات غير قابلة للكشف"""  
    ᴍᴀx_ᴄᴏɴᴄᴜʀʀᴇɴᴛ_ᴛᴇsᴛs = 25  
    ᴘʀᴏxʏ_ʀᴇғʀᴇsʜ_ᴍɪɴᴜᴛᴇs = 10  
    ᴛɪᴍᴇᴏᴜᴛ_ᴘʀɪᴍᴀʀʏ = 8.0  
    ᴛɪᴍᴇᴏᴜᴛ_ꜰᴀʟʟʙᴀᴄᴋ = 15.0  
    ᴍɪɴ_ᴘɪɴɢ_ᴍs = 500  
    ᴍᴀx_ᴘʀᴏxʏ_ᴀɢᴇ_ᴍɪɴᴜᴛᴇs = 30  
    ᴅɴs_ʀᴇsᴏʟᴠᴇʀs = ["8.8.8.8", "1.1.1.1", "9.9.9.9"]  
    ᴜsᴇʀ_ᴀɢᴇɴᴛ_ʀᴏᴛᴀᴛɪᴏɴ = True  
    ᴛʟs_ᴠᴇʀsɪᴏɴ = ssl.TLSVersion.TLSv1_3  
    ᴇɴᴀʙʟᴇ_ᴏʙꜰᴜsᴄᴀᴛɪᴏɴ = True  
    ᴍᴀx_ʀᴇᴛʀɪᴇs = 3  
    ʙᴀᴄᴋɢʀᴏᴜɴᴅ_ᴜᴘᴅᴀᴛᴇ = True  
  
# ========== ENUMS & DATA CLASSES ==========  
class __ᴘʀᴏxʏ_ᴛʏᴘᴇ(Enum):  
    """أنواع البروكسيات"""  
    ʜᴛᴛᴘ = "http"  
    ʜᴛᴛᴘs = "https"  
    sᴏᴄᴋs4 = "socks4"  
    sᴏᴄᴋs5 = "socks5"  
  
class __ᴘʀᴏxʏ_ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ(Enum):  
    """نتائج التحقق من البروكسي"""  
    ᴠᴀʟɪᴅ = auto()  
    ᴅᴀᴛᴀᴄᴇɴᴛᴇʀ = auto()  
    ᴠᴘɴ = auto()  
    ʙʟᴀᴄᴋʟɪsᴛᴇᴅ = auto()  
    ʜɪɢʜ_ʟᴀᴛᴇɴᴄʏ = auto()  
    ɴᴏ_ᴛʟs13 = auto()  
    ᴛɪᴍᴇᴏᴜᴛ = auto()  
  
class __ɢᴇᴏ_ʟᴇᴠᴇʟ(Enum):  
    """مستويات الموقع الجغرافي"""  
    ᴄᴏᴜɴᴛʀʏ = auto()  
    sᴛᴀᴛᴇ = auto()  
    ᴄɪᴛʏ = auto()  
    ᴢɪᴘᴄᴏᴅᴇ = auto()  
  
@dataclass  
class __ɢᴇᴏ_ʟᴏᴄᴀᴛɪᴏɴ:  
    """بيانات الموقع الجغرافي"""  
    ᴄᴏᴜɴᴛʀʏ: str  
    sᴛᴀᴛᴇ: Optional[str] = None  
    ᴄɪᴛʏ: Optional[str] = None  
    ᴢɪᴘᴄᴏᴅᴇ: Optional[str] = None  
    ʟᴀᴛɪᴛᴜᴅᴇ: Optional[float] = None  
    ʟᴏɴɢɪᴛᴜᴅᴇ: Optional[float] = None  
    ᴀsɴ: Optional[str] = None  
    ɪsᴘ: Optional[str] = None  
  
@dataclass  
class __ᴘʀᴏxʏ_ᴍᴇᴛᴀᴅᴀᴛᴀ:  
    """بيانات وصفية للبروكسي"""  
    ɪᴘ: str  
    ᴘᴏʀᴛ: int  
    ᴛʏᴘᴇ: __ᴘʀᴏxʏ_ᴛʏᴘᴇ  
    ɢᴇᴏ: __ɢᴇᴏ_ʟᴏᴄᴀᴛɪᴏɴ  
    ʟᴀsᴛ_ᴠᴇʀɪꜰɪᴇᴅ: datetime = field(default_factory=datetime.utcnow)  
    sᴜᴄᴄᴇss_ʀᴀᴛᴇ: float = 0.0  
    ᴀᴠᴇʀᴀɢᴇ_ʟᴀᴛᴇɴᴄʏ: float = 0.0  
    ʙᴀɴᴅᴡɪᴅᴛʜ_ᴍʙᴘs: float = 0.0  
    ɪs_ᴠᴘɴ: bool = False  
    ɪs_ᴅᴀᴛᴀᴄᴇɴᴛᴇʀ: bool = False  
    sᴜᴘᴘᴏʀᴛs_ᴛʟs13: bool = False  
    ʜᴀs_ᴋᴇᴇᴘ_ᴀʟɪᴠᴇ: bool = False  
    ᴜᴘᴛɪᴍᴇ_ᴍɪɴᴜᴛᴇs: int = 0  
    ꜰᴀɪʟᴜʀᴇ_ᴄᴏᴜɴᴛ: int = 0  
    ᴜɴɪǫᴜᴇ_ɪᴅ: str = field(default_factory=lambda: str(uuid.uuid4()))  
  
@dataclass  
class __ʀᴏᴜᴛɪɴɢ_ʀᴜʟᴇ:  
    """قاعدة توجيه جغرافية"""  
    ᴛᴀʀɢᴇᴛ_ʟᴏᴄᴀᴛɪᴏɴ: __ɢᴇᴏ_ʟᴏᴄᴀᴛɪᴏɴ  
    ᴘʀᴏxʏ_ʟᴏᴄᴀᴛɪᴏɴ: __ɢᴇᴏ_ʟᴏᴄᴀᴛɪᴏɴ  
    ᴍᴀx_ᴅɪsᴛᴀɴᴄᴇ_ᴋᴍ: float  
    ᴘʀɪᴏʀɪᴛʏ: int = 100  
  
# ========== COMPLETE US GEOGRAPHIC DATABASE ==========  
class __US__ɢᴇᴏ_ᴅᴀᴛᴀʙᴀsᴇ:  
    """قاعدة بيانات جغرافية كاملة للولايات المتحدة"""  
      
    # خرائط الدول والمدن الرئيسية مع الإحداثيات  
    ʙʏ_ᴢɪᴘ_ᴘʀᴇꜰɪx = {  
        "900": {"state": "CA", "city": "Los Angeles", "lat": 34.0522, "lon": -118.2437},  
        "902": {"state": "CA", "city": "Beverly Hills", "lat": 34.0736, "lon": -118.4004},  
        "606": {"state": "IL", "city": "Chicago", "lat": 41.8781, "lon": -87.6298},  
        "100": {"state": "NY", "city": "New York", "lat": 40.7128, "lon": -74.0060},  
        "752": {"state": "TX", "city": "Dallas", "lat": 32.7767, "lon": -96.7970},  
        "331": {"state": "FL", "city": "Miami", "lat": 25.7617, "lon": -80.1918},  
        "850": {"state": "FL", "city": "Tallahassee", "lat": 30.4383, "lon": -84.2807},  
        "303": {"state": "CO", "city": "Denver", "lat": 39.7392, "lon": -104.9903},  
        "981": {"state": "WA", "city": "Seattle", "lat": 47.6062, "lon": -122.3321},  
        "941": {"state": "CA", "city": "San Francisco", "lat": 37.7749, "lon": -122.4194},  
        "787": {"state": "PR", "city": "San Juan", "lat": 18.4655, "lon": -66.1057},  
        "968": {"state": "HI", "city": "Honolulu", "lat": 21.3069, "lon": -157.8583},  
        "995": {"state": "AK", "city": "Anchorage", "lat": 61.2181, "lon": -149.9003},  
    }  
      
    # مدن رئيسية لكل ولاية  
    ʙʏ_ᴜs_ᴍᴀᴊᴏʀ_ᴄɪᴛɪᴇs = {  
        "CA": ["Los Angeles", "San Francisco", "San Diego", "San Jose", "Fresno", "Sacramento"],  
        "TX": ["Houston", "Dallas", "Austin", "San Antonio", "El Paso", "Fort Worth"],  
        "FL": ["Miami", "Orlando", "Tampa", "Jacksonville", "Tallahassee", "Fort Lauderdale"],  
        "NY": ["New York City", "Buffalo", "Rochester", "Yonkers", "Syracuse", "Albany"],  
        "IL": ["Chicago", "Aurora", "Rockford", "Joliet", "Naperville", "Springfield"],  
        "PA": ["Philadelphia", "Pittsburgh", "Allentown", "Erie", "Reading", "Scranton"],  
        "OH": ["Columbus", "Cleveland", "Cincinnati", "Toledo", "Akron", "Dayton"],  
        "GA": ["Atlanta", "Augusta", "Columbus", "Macon", "Savannah", "Athens"],  
        "NC": ["Charlotte", "Raleigh", "Greensboro", "Durham", "Winston-Salem", "Fayetteville"],  
        "MI": ["Detroit", "Grand Rapids", "Warren", "Sterling Heights", "Ann Arbor", "Lansing"],  
    }  
      
    # إحداثيات مركزية لكل ولاية  
    ʙʏ_ᴜs_ᴡɪᴛʜ_ᴄᴏᴏʀᴅɪɴᴀᴛᴇs = {  
        "AL": {"capital": "Montgomery", "lat": 32.3770, "lon": -86.3006},  
        "AK": {"capital": "Juneau", "lat": 58.3019, "lon": -134.4197},  
        "AZ": {"capital": "Phoenix", "lat": 33.4484, "lon": -112.0740},  
        "AR": {"capital": "Little Rock", "lat": 34.7465, "lon": -92.2896},  
        "CA": {"capital": "Sacramento", "lat": 38.5816, "lon": -121.4944},  
        "CO": {"capital": "Denver", "lat": 39.7392, "lon": -104.9903},  
        "CT": {"capital": "Hartford", "lat": 41.7658, "lon": -72.6734},  
        "DE": {"capital": "Dover", "lat": 39.1582, "lon": -75.5244},  
        "FL": {"capital": "Tallahassee", "lat": 30.4383, "lon": -84.2807},  
        "GA": {"capital": "Atlanta", "lat": 33.7490, "lon": -84.3880},  
        "HI": {"capital": "Honolulu", "lat": 21.3069, "lon": -157.8583},  
        "ID": {"capital": "Boise", "lat": 43.6150, "lon": -116.2023},  
        "IL": {"capital": "Springfield", "lat": 39.7817, "lon": -89.6501},  
        "IN": {"capital": "Indianapolis", "lat": 39.7684, "lon": -86.1581},  
        "IA": {"capital": "Des Moines", "lat": 41.5868, "lon": -93.6250},  
        "KS": {"capital": "Topeka", "lat": 39.0473, "lon": -95.6752},  
        "KY": {"capital": "Frankfort", "lat": 38.2009, "lon": -84.8733},  
        "LA": {"capital": "Baton Rouge", "lat": 30.4515, "lon": -91.1871},  
        "ME": {"capital": "Augusta", "lat": 44.3106, "lon": -69.7795},  
        "MD": {"capital": "Annapolis", "lat": 38.9784, "lon": -76.4922},  
        "MA": {"capital": "Boston", "lat": 42.3601, "lon": -71.0589},  
        "MI": {"capital": "Lansing", "lat": 42.7325, "lon": -84.5555},  
        "MN": {"capital": "St. Paul", "lat": 44.9537, "lon": -93.0900},  
        "MS": {"capital": "Jackson", "lat": 32.2988, "lon": -90.1848},  
        "MO": {"capital": "Jefferson City", "lat": 38.5767, "lon": -92.1735},  
        "MT": {"capital": "Helena", "lat": 46.5891, "lon": -112.0391},  
        "NE": {"capital": "Lincoln", "lat": 40.8136, "lon": -96.7026},  
        "NV": {"capital": "Carson City", "lat": 39.1638, "lon": -119.7674},  
        "NH": {"capital": "Concord", "lat": 43.2081, "lon": -71.5376},  
        "NJ": {"capital": "Trenton", "lat": 40.2206, "lon": -74.7597},  
        "NM": {"capital": "Santa Fe", "lat": 35.6870, "lon": -105.9378},  
        "NY": {"capital": "Albany", "lat": 42.6526, "lon": -73.7562},  
        "NC": {"capital": "Raleigh", "lat": 35.7796, "lon": -78.6382},  
        "ND": {"capital": "Bismarck", "lat": 46.8083, "lon": -100.7837},  
        "OH": {"capital": "Columbus", "lat": 39.9612, "lon": -82.9988},  
        "OK": {"capital": "Oklahoma City", "lat": 35.4676, "lon": -97.5164},  
        "OR": {"capital": "Salem", "lat": 44.9429, "lon": -123.0351},  
        "PA": {"capital": "Harrisburg", "lat": 40.2732, "lon": -76.8867},  
        "RI": {"capital": "Providence", "lat": 41.8236, "lon": -71.4222},  
        "SC": {"capital": "Columbia", "lat": 34.0007, "lon": -81.0348},  
        "SD": {"capital": "Pierre", "lat": 44.3668, "lon": -100.3538},  
        "TN": {"capital": "Nashville", "lat": 36.1627, "lon": -86.7816},  
        "TX": {"capital": "Austin", "lat": 30.2672, "lon": -97.7431},  
        "UT": {"capital": "Salt Lake City", "lat": 40.7608, "lon": -111.8910},  
        "VT": {"capital": "Montpelier", "lat": 44.2601, "lon": -72.5754},  
        "VA": {"capital": "Richmond", "lat": 37.5407, "lon": -77.4360},  
        "WA": {"capital": "Olympia", "lat": 47.0379, "lon": -122.9007},  
        "WV": {"capital": "Charleston", "lat": 38.3498, "lon": -81.6326},  
        "WI": {"capital": "Madison", "lat": 43.0731, "lon": -89.4012},  
        "WY": {"capital": "Cheyenne", "lat": 41.1399, "lon": -104.8202},  
        "DC": {"capital": "Washington", "lat": 38.9072, "lon": -77.0369},  
    }  
      
    @classmethod  
    def ɢᴇᴛ_ʟᴏᴄᴀᴛɪᴏɴ_ʙʏ_ᴢɪᴘ(cls, zip_code: str) -> Optional[__ɢᴇᴏ_ʟᴏᴄᴀᴛɪᴏɴ]:  
        """الحصول على الموقع الجغرافي بناءً على الرمز البريدي"""  
        prefix = zip_code[:3]  
        if prefix in cls.ʙʏ_ᴢɪᴘ_ᴘʀᴇꜰɪx:  
            data = cls.ʙʏ_ᴢɪᴘ_ᴘʀᴇꜰɪx[prefix]  
            return __ɢᴇᴏ_ʟᴏᴄᴀᴛɪᴏɴ(  
                country="US",  
                state=data["state"],  
                city=data["city"],  
                zipcode=zip_code,  
                latitude=data["lat"],  
                longitude=data["lon"]  
            )  
        return None  
      
    @classmethod  
    def ɢᴇᴛ_ɴᴇᴀʀᴇsᴛ_ᴄɪᴛɪᴇs(cls, state: str, count: int = 3) -> List[str]:  
        """الحصول على أقرب المدن داخل الولاية"""  
        if state in cls.ʙʏ_ᴜs_ᴍᴀᴊᴏʀ_ᴄɪᴛɪᴇs:  
            return cls.ʙʏ_ᴜs_ᴍᴀᴊᴏʀ_ᴄɪᴛɪᴇs[state][:count]  
        return [cls.ʙʏ_ᴜs_ᴡɪᴛʜ_ᴄᴏᴏʀᴅɪɴᴀᴛᴇs.get(state, {}).get("capital", "Unknown")]  
  
# ========== PROXY SOURCE SCRAPER ==========  
class __ᴘʀᴏxʏ_ʜᴀʀᴠᴇsᴛᴇʀ:  
    """حاصد بروكسيات تلقائي من مصادر متعددة"""  
      
    def __init__(self):  
        self.ʟᴀsᴛ_ʜᴀʀᴠᴇsᴛ = None  
        self.ʜᴀʀᴠᴇsᴛ_ʟᴏᴄᴋ = Lock()  
        self.ʀᴇᴛʀɪᴇᴅ_ᴘʀᴏxɪᴇs = defaultdict(list)  
          
        # مصادر متنوعة ومتجددة  
        self.ʜᴀʀᴠᴇsᴛ_ᴜʀʟs = [  
            # HTTP Proxies  
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",  
            "https://www.proxy-list.download/api/v1/get?type=http",  
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all",  
            "https://openproxy.space/list/http",  
            "https://proxyspace.pro/http.txt",  
              
            # SOCKS5 Proxies  
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",  
            "https://www.proxy-list.download/api/v1/get?type=socks5",  
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all",  
            "https://openproxy.space/list/socks5",  
            "https://proxyspace.pro/socks5.txt",  
              
            # Premium Sources  
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy-list/data.txt",  
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt",  
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt",  
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTP_RAW.txt",  
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",  
              
            # Country-Specific Sources  
            "https://www.proxy-list.download/api/v1/get?type=http&country=US",  
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&country=US",  
            "https://www.proxy-list.download/api/v1/get?type=http&country=GB",  
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&country=DE",  
            "https://www.proxy-list.download/api/v1/get?type=http&country=CA",  
        ]  
      
    async def ʜᴀʀᴠᴇsᴛ_ᴘʀᴏxɪᴇs(self) -> List[Tuple[str, int, str]]:  
        """حصاد بروكسيات من جميع المصادر"""  
        async with self.ʜᴀʀᴠᴇsᴛ_ʟᴏᴄᴋ:  
            if self.ʟᴀsᴛ_ʜᴀʀᴠᴇsᴛ and (datetime.utcnow() - self.ʟᴀsᴛ_ʜᴀʀᴠᴇsᴛ).seconds < 600:  
                return []  
              
            all_proxies = []  
            tasks = [self.__ʜᴀʀᴠᴇsᴛ_ꜰʀᴏᴍ_ᴜʀʟ(url) for url in self.ʜᴀʀᴠᴇsᴛ_ᴜʀʟs]  
            results = await asyncio.gather(*tasks, return_exceptions=True)  
              
            for result in results:  
                if isinstance(result, list):  
                    all_proxies.extend(result)  
              
            # إزالة التكرارات  
            unique_proxies = list(set(all_proxies))  
            self.ʟᴀsᴛ_ʜᴀʀᴠᴇsᴛ = datetime.utcnow()  
              
            logging.info(f"🌱 Harvested {len(unique_proxies)} proxies")  
            return unique_proxies  
      
    async def __ʜᴀʀᴠᴇsᴛ_ꜰʀᴏᴍ_ᴜʀʟ(self, url: str) -> List[Tuple[str, int, str]]:  
        """حصاد من عنوان URL فردي"""  
        try:  
            timeout = aiohttp.ClientTimeout(total=15)  
            async with aiohttp.ClientSession(timeout=timeout) as session:  
                headers = {  
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',  
                    'Accept': 'text/plain,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',  
                    'Accept-Language': 'en-US,en;q=0.5',  
                    'Accept-Encoding': 'gzip, deflate',  
                    'DNT': '1',  
                    'Connection': 'keep-alive',  
                    'Upgrade-Insecure-Requests': '1'  
                }  
                  
                async with session.get(url, headers=headers, ssl=False) as response:  
                    if response.status == 200:  
                        content = await response.text()  
                        return self.__ᴘᴀʀsᴇ_ᴘʀᴏxʏ_ʟɪsᴛ(content, url)  
        except Exception as e:  
            logging.debug(f"Failed to harvest from {url}: {e}")  
          
        return []  
      
    def __ᴘᴀʀsᴇ_ᴘʀᴏxʏ_ʟɪsᴛ(self, content: str, source_url: str) -> List[Tuple[str, int, str]]:  
        """تحليل قائمة البروكسيات"""  
        proxies = []  
        lines = content.strip().split('\n')  
          
        for line in lines:  
            line = line.strip()  
            if not line or line.startswith('#'):  
                continue  
              
            # تنسيقات مختلفة للبروكسيات  
            patterns = [  
                r'(\d+\.\d+\.\d+\.\d+):(\d+)',  # IP:Port  
                r'(\d+\.\d+\.\d+\.\d+)\s+(\d+)', # IP Port  
                r'http://(\d+\.\d+\.\d+\.\d+):(\d+)', # http://IP:Port  
                r'socks5://(\d+\.\d+\.\d+\.\d+):(\d+)', # socks5://IP:Port  
            ]  
              
            for pattern in patterns:  
                match = re.match(pattern, line)  
                if match:  
                    ip = match.group(1)  
                    port = int(match.group(2))  
                      
                    # تحديد النوع من المصدر  
                    if 'socks5' in source_url or 'socks5' in line:  
                        proxy_type = 'socks5'  
                    elif 'socks4' in source_url or 'socks4' in line:  
                        proxy_type = 'socks4'  
                    elif 'https' in source_url:  
                        proxy_type = 'https'  
                    else:  
                        proxy_type = 'http'  
                      
                    proxies.append((ip, port, proxy_type))  
                    break  
          
        return proxies  
  
# ========== ADVANCED PROXY VALIDATOR ==========  
class __ᴘʀᴏxʏ_ᴊᴜᴅɢᴇ:  
    """قاضي بروكسيات متقدم مع تحقق متعدد الطبقات"""  
      
    def __init__(self):  
        self.ᴠᴘɴ_ɪᴘ_ʀᴀɴɢᴇs = self.__ʟᴏᴀᴅ_ᴠᴘɴ_ʀᴀɴɢᴇs()  
        self.ᴅᴀᴛᴀᴄᴇɴᴛᴇʀ_ᴀsɴs = self.__ʟᴏᴀᴅ_ᴅᴄ_ᴀsɴs()  
        self.ʙʟᴀᴄᴋʟɪsᴛ_ɪᴘs = set()  
        self.ᴠᴀʟɪᴅᴀᴛɪᴏɴ_ʟᴏᴄᴋ = Lock()  
      
    def __ʟᴏᴀᴅ_ᴠᴘɴ_ʀᴀɴɢᴇs(self) -> List[Tuple[ipaddress.IPv4Network, str]]:  
        """تحميل نطاقات IPs الخاصة بموفرين VPN"""  
        vpn_ranges = []  
        # نطاقات AWS  
        vpn_ranges.extend([  
            (ipaddress.ip_network('3.0.0.0/9'), 'AWS'),  
            (ipaddress.ip_network('52.0.0.0/10'), 'AWS'),  
            (ipaddress.ip_network('54.0.0.0/8'), 'AWS'),  
        ])  
        # نطاقات GCP  
        vpn_ranges.extend([  
            (ipaddress.ip_network('8.34.0.0/16'), 'GCP'),  
            (ipaddress.ip_network('8.35.0.0/16'), 'GCP'),  
            (ipaddress.ip_network('34.0.0.0/8'), 'GCP'),  
        ])  
        # نطاقات Azure  
        vpn_ranges.extend([  
            (ipaddress.ip_network('13.64.0.0/11'), 'Azure'),  
            (ipaddress.ip_network('20.0.0.0/10'), 'Azure'),  
            (ipaddress.ip_network('40.0.0.0/8'), 'Azure'),  
        ])  
        # نطاقات DigitalOcean  
        vpn_ranges.extend([  
            (ipaddress.ip_network('138.197.0.0/16'), 'DigitalOcean'),  
            (ipaddress.ip_network('159.203.0.0/16'), 'DigitalOcean'),  
            (ipaddress.ip_network('104.131.0.0/16'), 'DigitalOcean'),  
        ])  
        return vpn_ranges  
      
    def __ʟᴏᴀᴅ_ᴅᴄ_ᴀsɴs(self) -> Set[str]:  
        """تحميل أرقام ASN لمراكز البيانات"""  
        return {  
            'AS14618',  # Amazon  
            'AS15169',  # Google  
            'AS8075',   # Microsoft  
            'AS16276',  # OVH  
            'AS14061',  # DigitalOcean  
            'AS12876',  # Online SAS  
            'AS20473',  # Choopa  
            'AS24940',  # Hetzner  
            'AS2906',   # NFOrce  
            'AS63311',  # Linode  
        }  
      
    async def ᴊᴜᴅɢᴇ_ᴘʀᴏxʏ(self, proxy_meta: __ᴘʀᴏxʏ_ᴍᴇᴛᴀᴅᴀᴛᴀ) -> Tuple[__ᴘʀᴏxʏ_ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ, Dict[str, Any]]:  
        """تحقق متقدم من البروكسي"""  
        validation_results = {}  
          
        try:  
            # 1. التحقق من VPN/DataCenter  
            ip_obj = ipaddress.ip_address(proxy_meta.ɪᴘ)  
            is_vpn = False  
            is_datacenter = False  
              
            for network, provider in self.ᴠᴘɴ_ɪᴘ_ʀᴀɴɢᴇs:  
                if ip_obj in network:  
                    is_vpn = True  
                    validation_results['vpn_provider'] = provider  
                    break  
              
            if proxy_meta.ɢᴇᴏ.ᴀsɴ in self.ᴅᴀᴛᴀᴄᴇɴᴛᴇʀ_ᴀsɴs:  
                is_datacenter = True  
              
            if is_vpn or is_datacenter:  
                return (__ᴘʀᴏxʏ_ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ.ᴠᴘɴ if is_vpn else __ᴘʀᴏxʏ_ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ.ᴅᴀᴛᴀᴄᴇɴᴛᴇʀ, validation_results)  
              
            # 2. اختبار TLS 1.3  
            tls_supported = await self.__ᴛᴇsᴛ_ᴛʟs13(proxy_meta)  
            if not tls_supported:  
                return (__ᴘʀᴏxʏ_ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ.ɴᴏ_ᴛʟs13, validation_results)  
              
            # 3. اختبار الكمون  
            latency = await self.__ᴛᴇsᴛ_ʟᴀᴛᴇɴᴄʏ(proxy_meta)  
            if latency > __ᴄᴏɴғɪɢ.ᴍɪɴ_ᴘɪɴɢ_ᴍs:  
                return (__ᴘʀᴏxʏ_ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ.ʜɪɢʜ_ʟᴀᴛᴇɴᴄʏ, validation_results)  
              
            # 4. اختبار Keep-Alive  
            keep_alive = await self.__ᴛᴇsᴛ_ᴋᴇᴇᴘ_ᴀʟɪᴠᴇ(proxy_meta)  
              
            validation_results.update({  
                'latency_ms': latency,  
                'tls13_supported': tls_supported,  
                'keep_alive': keep_alive,  
                'bandwidth_mbps': await self.__ᴛᴇsᴛ_ʙᴀɴᴅᴡɪᴅᴛʜ(proxy_meta),  
            })  
              
            return (__ᴘʀᴏxʏ_ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ.ᴠᴀʟɪᴅ, validation_results)  
              
        except asyncio.TimeoutError:  
            return (__ᴘʀᴏxʏ_ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ.ᴛɪᴍᴇᴏᴜᴛ, validation_results)  
        except Exception as e:  
            logging.debug(f"Proxy validation failed: {e}")  
            return (__ᴘʀᴏxʏ_ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ.ʙʟᴀᴄᴋʟɪsᴛᴇᴅ, validation_results)  
      
    async def __ᴛᴇsᴛ_ᴛʟs13(self, proxy_meta: __ᴘʀᴏxʏ_ᴍᴇᴛᴀᴅᴀᴛᴀ) -> bool:  
        """اختبار دعم TLS 1.3"""  
        try:  
            ssl_context = ssl.create_default_context()  
            ssl_context.minimum_version = ssl.TLSVersion.TLSv1_3  
              
            connector = aiohttp.TCPConnector(ssl=ssl_context)  
            proxy_url = f"{proxy_meta.ᴛʏᴘᴇ.value}://{proxy_meta.ɪᴘ}:{proxy_meta.ᴘᴏʀᴛ}"  
              
            timeout = aiohttp.ClientTimeout(total=10)  
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:  
                async with session.get('https://httpbin.org/get', proxy=proxy_url) as response:  
                    return response.status == 200  
        except:  
            return False  
      
    async def __ᴛᴇsᴛ_ʟᴀᴛᴇɴᴄʏ(self, proxy_meta: __ᴘʀᴏxʏ_ᴍᴇᴛᴀᴅᴀᴛᴀ) -> float:  
        """قياس الكمون"""  
        try:  
            start = time.time()  
            reader, writer = await asyncio.wait_for(  
                asyncio.open_connection(proxy_meta.ɪᴘ, proxy_meta.ᴘᴏʀᴛ),  
                timeout=5  
            )  
            writer.close()  
            await writer.wait_closed()  
            return (time.time() - start) * 1000  # Convert to ms  
        except:  
            return float('inf')  
      
    async def __ᴛᴇsᴛ_ᴋᴇᴇᴘ_ᴀʟɪᴠᴇ(self, proxy_meta: __ᴘʀᴏxʏ_ᴍᴇᴛᴀᴅᴀᴛᴀ) -> bool:  
        """اختبار دعم Keep-Alive"""  
        try:  
            proxy_url = f"{proxy_meta.ᴛʏᴘᴇ.value}://{proxy_meta.ɪᴘ}:{proxy_meta.ᴘᴏʀᴛ}"  
            async with aiohttp.ClientSession() as session:  
                # طلبين متتاليين  
                async with session.get('https://httpbin.org/get', proxy=proxy_url) as r1:  
                    if r1.status != 200:  
                        return False  
                    headers1 = dict(r1.headers)  
                  
                async with session.get('https://httpbin.org/get', proxy=proxy_url) as r2:  
                    if r2.status != 200:  
                        return False  
                  
                # التحقق من وجود Keep-Alive في الردود  
                return 'keep-alive' in str(headers1).lower()  
        except:  
            return False  
      
    async def __ᴛᴇsᴛ_ʙᴀɴᴅᴡɪᴅᴛʜ(self, proxy_meta: __ᴘʀᴏxʏ_ᴍᴇᴛᴀᴅᴀᴛᴀ) -> float:  
        """قياس عرض النطاق الترددي"""  
        try:  
            proxy_url = f"{proxy_meta.ᴛʏᴘᴇ.value}://{proxy_meta.ɪᴘ}:{proxy_meta.ᴘᴏʀᴛ}"  
            test_url = "https://speedtest.ftp.otenet.gr/files/test1Mb.db"  
              
            start = time.time()  
            async with aiohttp.ClientSession() as session:  
                async with session.get(test_url, proxy=proxy_url, timeout=30) as response:  
                    content = await response.read()  
                    elapsed = time.time() - start  
                    size_mb = len(content) / (1024 * 1024)  
                    return size_mb / elapsed if elapsed > 0 else 0  
        except:  
            return 0.0  
  
# ========== HEADER FACTORY FOR ANTI-FINGERPRINTING ==========  
class __ʜᴇᴀᴅᴇʀ_ɢᴇɴᴇʀᴀᴛᴏʀ:  
    """مولد عناوين HTTP فريدة لمكافحة البصمة"""  
      
    def __init__(self):  
        self.ᴜsᴇʀ_ᴀɢᴇɴᴛs = [  
            # Chrome on Windows  
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',  
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',  
            # Firefox on Windows  
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',  
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',  
            # Safari on Mac  
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',  
            # Chrome on Mac  
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',  
            # Mobile Chrome  
            'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',  
        ]  
          
        self.ʟᴀɴɢᴜᴀɢᴇs = {  
            'US': ['en-US,en;q=0.9', 'en;q=0.8'],  
            'GB': ['en-GB,en;q=0.9', 'en;q=0.8'],  
            'CA': ['en-CA,en;q=0.9', 'fr-CA,fr;q=0.8,en;q=0.7'],  
            'DE': ['de-DE,de;q=0.9,en;q=0.8'],  
            'FR': ['fr-FR,fr;q=0.9,en;q=0.8'],  
            'ES': ['es-ES,es;q=0.9,en;q=0.8'],  
        }  
          
        self.ᴀᴄᴄᴇᴘᴛ_ᴇɴᴄᴏᴅɪɴɢs = [  
            'gzip, deflate, br',  
            'gzip, deflate',  
            'br, gzip, deflate',  
        ]  
          
        self.ʀᴇꜰᴇʀᴇʀs = [  
            'https://www.google.com/',  
            'https://www.bing.com/',  
            'https://duckduckgo.com/',  
            'https://www.facebook.com/',  
            'https://www.reddit.com/',  
            'https://twitter.com/',  
            'https://www.amazon.com/',  
            'https://www.youtube.com/',  
        ]  
      
    def ɢᴇɴᴇʀᴀᴛᴇ_ʜᴇᴀᴅᴇʀs(self, country_code: str = 'US') -> Dict[str, str]:  
        """توليد عناوين HTTP فريدة"""  
        headers = {  
            'User-Agent': random.choice(self.ᴜsᴇʀ_ᴀɢᴇɴᴛs),  
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',  
            'Accept-Language': random.choice(self.ʟᴀɴɢᴜᴀɢᴇs.get(country_code, self.ʟᴀɴɢᴜᴀɢᴇs['US'])),  
            'Accept-Encoding': random.choice(self.ᴀᴄᴄᴇᴘᴛ_ᴇɴᴄᴏᴅɪɴɢs),  
            'DNT': random.choice(['1', '0']),  
            'Connection': random.choice(['keep-alive', 'close']),  
            'Upgrade-Insecure-Requests': '1',  
            'Sec-Fetch-Dest': 'document',  
            'Sec-Fetch-Mode': 'navigate',  
            'Sec-Fetch-Site': random.choice(['none', 'cross-site', 'same-origin']),  
            'Sec-Fetch-User': '?1',  
            'Cache-Control': random.choice(['max-age=0', 'no-cache']),  
            'Pragma': random.choice(['no-cache', '']),  
        }  
          
        # إضافة Client Hints بشكل عشوائي  
        if random.random() > 0.5:  
            headers.update({  
                'Sec-CH-UA': '"Chromium";v="120", "Google Chrome";v="120", "Not=A?Brand";v="99"',  
                'Sec-CH-UA-Mobile': '?0',  
                'Sec-CH-UA-Platform': '"Windows"',  
            })  
          
        # إضافة Referer بشكل عشوائي  
        if random.random() > 0.3:  
            headers['Referer'] = random.choice(self.ʀᴇꜰᴇʀᴇʀs)  
          
        return headers  
  
# ========== MAIN PROXY ORCHESTRATOR ==========  
class __ɢᴇᴏ_ᴘʀᴏxʏ_ᴏʀᴄʜᴇsᴛʀᴀᴛᴏʀ:  
    """مدرس بروكسيات جغرافي متقدم"""  
      
    def __init__(self):  
        self.ʜᴀʀᴠᴇsᴛᴇʀ = __ᴘʀᴏxʏ_ʜᴀʀᴠᴇsᴛᴇʀ()  
        self.ᴊᴜᴅɢᴇ = __ᴘʀᴏxʏ_ᴊᴜᴅɢᴇ()  
        self.ʜᴇᴀᴅᴇʀ_ɢᴇɴ = __ʜᴇᴀᴅᴇʀ_ɢᴇɴᴇʀᴀᴛᴏʀ()  
          
        self.ᴀᴄᴛɪᴠᴇ_ᴘʀᴏxɪᴇs: Dict[str, __ᴘʀᴏxʏ_ᴍᴇᴛᴀᴅᴀᴛᴀ] = {}  
        self.ɢᴇᴏ_ɪɴᴅᴇx: Dict[str, List[str]] = defaultdict(list)  
        self.sᴛɪᴄᴋʏ_ᴛᴀsᴋs: Dict[str, str] = {}  # task_id -> proxy_id  
        self.ʀᴏᴛᴀᴛɪᴏɴ_ᴄᴏᴜɴᴛᴇʀ: Dict[str, int] = defaultdict(int)  
          
        self.ᴛᴀsᴋ_ǫᴜᴇᴜᴇ = Queue()  
        self.ᴏʀᴄʜᴇsᴛʀᴀᴛɪᴏɴ_ʟᴏᴄᴋ = Lock()  
        self.ʀᴜɴɴɪɴɢ = False  
          
        self.ʟᴏɢɢᴇʀ = self.__sᴇᴛᴜᴘ_ʟᴏɢɢɪɴɢ()  
      
    def __sᴇᴛᴜᴘ_ʟᴏɢɢɪɴɢ(self) -> logging.Logger:  
        """إعداد نظام التسجيل المتقدم"""  
        logger = logging.getLogger('GeoProxyOrchestrator')  
        logger.setLevel(logging.INFO)  
          
        # Formatter مع تشفير المعلومات الحساسة  
        class __ᴍᴀsᴋᴇᴅ_ꜰᴏʀᴍᴀᴛᴛᴇʀ(logging.Formatter):  
            def format(self, record):  
                msg = super().format(record)  
                # تشفير عناوين IP في السجلات  
                msg = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',   
                           lambda m: hashlib.md5(m.group().encode()).hexdigest()[:8], msg)  
                return msg  
          
        handler = logging.StreamHandler()  
        handler.setFormatter(__ᴍᴀsᴋᴇᴅ_ꜰᴏʀᴍᴀᴛᴛᴇʀ(  
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'  
        ))  
        logger.addHandler(handler)  
          
        return logger  
      
    async def ɪɴɪᴛɪᴀʟɪᴢᴇ(self):  
        """تهيئة النظام"""  
        self.ʟᴏɢɢᴇʀ.info("🚀 Initializing Geo-Proxy Orchestrator v6.0.0")  
        self.ʀᴜɴɴɪɴɢ = True  
          
        # بدء حصاد الخلفية  
        if __ᴄᴏɴғɪɢ.ʙᴀᴄᴋɢʀᴏᴜɴᴅ_ᴜᴘᴅᴀᴛᴇ:  
            asyncio.create_task(self.__ʙᴀᴄᴋɢʀᴏᴜɴᴅ_ʜᴀʀᴠᴇsᴛᴇʀ())  
          
        # تحميل البروكسيات الأولية  
        await self.__ʟᴏᴀᴅ_ɪɴɪᴛɪᴀʟ_ᴘʀᴏxɪᴇs()  
          
        self.ʟᴏɢɢᴇʀ.info(f"✅ Initialized with {len(self.ᴀᴄᴛɪᴠᴇ_ᴘʀᴏxɪᴇs)} validated proxies")  
      
    async def __ʟᴏᴀᴅ_ɪɴɪᴛɪᴀʟ_ᴘʀᴏxɪᴇs(self):  
        """تحميل وتدقيق البروكسيات الأولية"""  
        raw_proxies = await self.ʜᴀʀᴠᴇsᴛᴇʀ.ʜᴀʀᴠᴇsᴛ_ᴘʀᴏxɪᴇs()  
          
        validation_tasks = []  
        for ip, port, proxy_type in raw_proxies[:100]:  # الحد الأولي  
            proxy_meta = __ᴘʀᴏxʏ_ᴍᴇᴛᴀᴅᴀᴛᴀ(  
                ip=ip,  
                port=port,  
                type=__ᴘʀᴏxʏ_ᴛʏᴘᴇ(proxy_type),  
                geo=await self.__ɢᴇᴛ_ɢᴇᴏ_ɪɴꜰᴏ(ip)  
            )  
            validation_tasks.append(self.__ᴠᴀʟɪᴅᴀᴛᴇ_ᴀɴᴅ_ᴀᴅᴅ_ᴘʀᴏxʏ(proxy_meta))  
          
        await asyncio.gather(*validation_tasks)  
      
    async def __ɢᴇᴛ_ɢᴇᴏ_ɪɴꜰᴏ(self, ip: str) -> __ɢᴇᴏ_ʟᴏᴄᴀᴛɪᴏɴ:  
        """الحصول على المعلومات الجغرافية لـ IP"""  
        # محاكاة API جغرافي (في الإنتاج استخدم ipinfo.io أو مشابه)  
        try:  
            # هنا يمكنك استخدام ipinfo.io API  
            # async with aiohttp.ClientSession() as session:  
            #     async with session.get(f'https://ipinfo.io/{ip}/json') as resp:  
            #         data = await resp.json()  
              
            # محاكاة للتوضيح  
            country = random.choice(['US', 'GB', 'DE', 'FR', 'CA'])  
            state = random.choice(['CA', 'TX', 'FL', 'NY', 'IL']) if country == 'US' else None  
            city = random.choice(['New York', 'Los Angeles', 'Chicago']) if state else None  
              
            return __ɢᴇᴏ_ʟᴏᴄᴀᴛɪᴏɴ(  
                country=country,  
                state=state,  
                city=city,  
                asn=f"AS{random.randint(1000, 99999)}",  
                isp=random.choice(['Comcast', 'AT&T', 'Verizon', 'Spectrum'])  
            )  
        except:  
            return __ɢᴇᴏ_ʟᴏᴄᴀᴛɪᴏɴ(country='Unknown')  
      
    async def __ᴠᴀʟɪᴅᴀᴛᴇ_ᴀɴᴅ_ᴀᴅᴅ_ᴘʀᴏxʏ(self, proxy_meta: __ᴘʀᴏxʏ_ᴍᴇᴛᴀᴅᴀᴛᴀ):  
        """التحقق من البروكسي وإضافته إذا كان صالحاً"""  
        result, details = await self.ᴊᴜᴅɢᴇ.ᴊᴜᴅɢᴇ_ᴘʀᴏxʏ(proxy_meta)  
          
        if result == __ᴘʀᴏxʏ_ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ.ᴠᴀʟɪᴅ:  
            # تحديث البيانات الوصفية  
            proxy_meta.ᴀᴠᴇʀᴀɢᴇ_ʟᴀᴛᴇɴᴄʏ = details.get('latency_ms', 0)  
            proxy_meta.sᴜᴘᴘᴏʀᴛs_ᴛʟs13 = details.get('tls13_supported', False)  
            proxy_meta.ʜᴀs_ᴋᴇᴇᴘ_ᴀʟɪᴠᴇ = details.get('keep_alive', False)  
            proxy_meta.ʙᴀɴᴅᴡɪᴅᴛʜ_ᴍʙᴘs = details.get('bandwidth_mbps', 0)  
              
            # إضافة إلى الفهرس  
            proxy_id = proxy_meta.ᴜɴɪǫᴜᴇ_ɪᴅ  
            self.ᴀᴄᴛɪᴠᴇ_ᴘʀᴏxɪᴇs[proxy_id] = proxy_meta  
              
            # فهرسة جغرافية  
            geo_key = f"{proxy_meta.ɢᴇᴏ.ᴄᴏᴜɴᴛʀʏ}_{proxy_meta.ɢᴇᴏ.sᴛᴀᴛᴇ or 'ANY'}"  
            self.ɢᴇᴏ_ɪɴᴅᴇx[geo_key].append(proxy_id)  
              
            self.ʟᴏɢɢᴇʀ.debug(f"✅ Added proxy {proxy_id} from {proxy_meta.ɢᴇᴏ.ᴄᴏᴜɴᴛʀʏ}/{proxy_meta.ɢᴇᴏ.sᴛᴀᴛᴇ}")  
      
    async def __ʙᴀᴄᴋɢʀᴏᴜɴᴅ_ʜᴀʀᴠᴇsᴛᴇʀ(self):  
        """حصاد خلفي تلقائي"""  
        while self.ʀᴜɴɴɪɴɢ:  
            try:  
                await asyncio.sleep(600)  # كل 10 دقائق  
                await self.__ʀᴇꜰʀᴇsʜ_ᴘʀᴏxɪᴇs()  
            except Exception as e:  
                self.ʟᴏɢɢᴇʀ.error(f"Background harvester error: {e}")  
      
    async def __ʀᴇꜰʀᴇsʜ_ᴘʀᴏxɪᴇs(self):  
        """تحديث مجموعة البروكسيات"""  
        self.ʟᴏɢɢᴇʀ.info("🔄 Refreshing proxy pool")  
          
        # إزالة البروكسيات القديمة  
        now = datetime.utcnow()  
        expired_keys = []  
        for proxy_id, proxy in self.ᴀᴄᴛɪᴠᴇ_ᴘʀᴏxɪᴇs.items():  
            if (now - proxy.ʟᴀsᴛ_ᴠᴇʀɪꜰɪᴇᴅ).seconds > 1800:  # 30 دقيقة  
                expired_keys.append(proxy_id)  
          
        for key in expired_keys:  
            del self.ᴀᴄᴛɪᴠᴇ_ᴘʀᴏxɪᴇs[key]  
          
        # حصاد بروكسيات جديدة  
        await self.__ʟᴏᴀᴅ_ɪɴɪᴛɪᴀʟ_ᴘʀᴏxɪᴇs()  
      
    async def ɢᴇᴛ_ᴘʀᴏxʏ_ꜰᴏʀ_ʟᴏᴄᴀᴛɪᴏɴ(self, target_location: __ɢᴇᴏ_ʟᴏᴄᴀᴛɪᴏɴ,   
                                       task_id: Optional[str] = None) -> Optional[__ᴘʀᴏxʏ_ᴍᴇᴛᴀᴅᴀᴛᴀ]:  
        """الحصول على بروكسي مناسب للموقع الجغرافي"""  
        try:  
            # 1. التحقق من الجلسات اللاصقة  
            if task_id and task_id in self.sᴛɪᴄᴋʏ_ᴛᴀsᴋs:  
                proxy_id = self.sᴛɪᴄᴋʏ_ᴛᴀsᴋs[task_id]  
                if proxy_id in self.ᴀᴄᴛɪᴠᴇ_ᴘʀᴏxɪᴇs:  
                    proxy = self.ᴀᴄᴛɪᴠᴇ_ᴘʀᴏxɪᴇs[proxy_id]  
                    self.ʀᴏᴛᴀᴛɪᴏɴ_ᴄᴏᴜɴᴛᴇʀ[task_id] += 1  
                      
                    # تدوير بعد 3 بطاقات  
                    if self.ʀᴏᴛᴀᴛɪᴏɴ_ᴄᴏᴜɴᴛᴇʀ[task_id] >= 3:  
                        self.__ʀᴏᴛᴀᴛᴇ_ᴛᴀsᴋ_ᴘʀᴏxʏ(task_id)  
                      
                    return proxy  
              
            # 2. البحث عن أفضل بروكسي جغرافياً  
            candidate_ids = []  
              
            # البحث بنفس البلد والولاية  
            if target_location.state:  
                geo_key = f"{target_location.country}_{target_location.state}"  
                candidate_ids.extend(self.ɢᴇᴏ_ɪɴᴅᴇx.get(geo_key, []))  
              
            # البحث بنفس البلد فقط  
            if not candidate_ids:  
                geo_key = f"{target_location.country}_ANY"  
                candidate_ids.extend(self.ɢᴇᴏ_ɪɴᴅᴇx.get(geo_key, []))  
              
            # إذا لم يوجد، استخدم أي بروكسي  
            if not candidate_ids:  
                candidate_ids = list(self.ᴀᴄᴛɪᴠᴇ_ᴘʀᴏxɪᴇs.keys())  
              
            # ترشيح أفضل البروكسيات بناءً على الأداء  
            candidates = []  
            for proxy_id in candidate_ids:  
                proxy = self.ᴀᴄᴛɪᴠᴇ_ᴘʀᴏxɪᴇs[proxy_id]  
                if proxy.ꜰᴀɪʟᴜʀᴇ_ᴄᴏᴜɴᴛ > 3:  
                    continue  
                  
                # حساب النقاط  
                score = (  
                    (1000 - proxy.ᴀᴠᴇʀᴀɢᴇ_ʟᴀᴛᴇɴᴄʏ) * 0.5 +  
                    proxy.sᴜᴄᴄᴇss_ʀᴀᴛᴇ * 100 * 0.3 +  
                    proxy.ʙᴀɴᴅᴡɪᴅᴛʜ_ᴍʙᴘs * 0.2  
                )  
                candidates.append((score, proxy_id, proxy))  
              
            if not candidates:  
                return None  
              
            # اختيار أفضل 5 وأخذ واحد عشوائي منهم (لتفادي الأنماط)  
            candidates.sort(reverse=True)  
            best_candidates = candidates[:5]  
            _, selected_id, selected_proxy = random.choice(best_candidates)  
              
            # 3. تعيين بروكسي للمهمة إذا كانت لاصقة  
            if task_id:  
                self.sᴛɪᴄᴋʏ_ᴛᴀsᴋs[task_id] = selected_id  
                self.ʀᴏᴛᴀᴛɪᴏɴ_ᴄᴏᴜɴᴛᴇʀ[task_id] = 1  
              
            return selected_proxy  
              
        except Exception as e:  
            self.ʟᴏɢɢᴇʀ.error(f"Error getting proxy for location: {e}")  
            return None  
      
    def __ʀᴏᴛᴀᴛᴇ_ᴛᴀsᴋ_ᴘʀᴏxʏ(self, task_id: str):  
        """تدوير بروكسي المهمة"""  
        if task_id in self.sᴛɪᴄᴋʏ_ᴛᴀsᴋs:  
            old_proxy_id = self.sᴛɪᴄᴋʏ_ᴛᴀsᴋs[task_id]  
              
            # زيادة عداد الفشل للبروكسي القديم  
            if old_proxy_id in self.ᴀᴄᴛɪᴠᴇ_ᴘʀᴏxɪᴇs:  
                self.ᴀᴄᴛɪᴠᴇ_ᴘʀᴏxɪᴇs[old_proxy_id].ꜰᴀɪʟᴜʀᴇ_ᴄᴏᴜɴᴛ += 1  
              
            # إزالة التعيين  
            del self.sᴛɪᴄᴋʏ_ᴛᴀsᴋs[task_id]  
            del self.ʀᴏᴛᴀᴛɪᴏɴ_ᴄᴏᴜɴᴛᴇʀ[task_id]  
      
    async def ʀᴇᴘᴏʀᴛ_ᴘʀᴏxʏ_ꜰᴀɪʟᴜʀᴇ(self, proxy_id: str, reason: str = "Unknown"):  
        """تقرير فشل بروكسي"""  
        try:  
            if proxy_id in self.ᴀᴄᴛɪᴠᴇ_ᴘʀᴏxɪᴇs:  
                proxy = self.ᴀᴄᴛɪᴠᴇ_ᴘʀᴏxɪᴇs[proxy_id]  
                proxy.ꜰᴀɪʟᴜʀᴇ_ᴄᴏᴜɴᴛ += 1  
                proxy.sᴜᴄᴄᴇss_ʀᴀᴛᴇ = max(0, proxy.sᴜᴄᴄᴇss_ʀᴀᴛᴇ - 0.1)  
                  
                self.ʟᴏɢɢᴇʀ.warning(f"Proxy {proxy_id} failed: {reason}")  
                  
                # إذا فشل أكثر من 5 مرات، إزالته  
                if proxy.ꜰᴀɪʟᴜʀᴇ_ᴄᴏᴜɴᴛ > 5:  
                    self.__ʀᴇᴍᴏᴠᴇ_ᴘʀᴏxʏ(proxy_id)  
                      
        except Exception as e:  
            self.ʟᴏɢɢᴇʀ.error(f"Error reporting proxy failure: {e}")  
      
    def __ʀᴇᴍᴏᴠᴇ_ᴘʀᴏxʏ(self, proxy_id: str):  
        """إزالة بروكسي من النظام"""  
        if proxy_id in self.ᴀᴄᴛɪᴠᴇ_ᴘʀᴏxɪᴇs:  
            del self.ᴀᴄᴛɪᴠᴇ_ᴘʀᴏxɪᴇs[proxy_id]  
              
            # إزالة من الفهرس الجغرافي  
            for geo_key, proxy_ids in self.ɢᴇᴏ_ɪɴᴅᴇx.items():  
                if proxy_id in proxy_ids:  
                    proxy_ids.remove(proxy_id)  
      
    async def ᴄʀᴇᴀᴛᴇ_ᴘʀᴏxʏ_ᴄʟɪᴇɴᴛ(self, target_location: __ɢᴇᴏ_ʟᴏᴄᴀᴛɪᴏɴ,   
                                  task_id: Optional[str] = None) -> Optional[aiohttp.ClientSession]:  
        """إنشاء عميل HTTP مع بروكسي مناسب"""  
        try:  
            proxy_meta = await self.ɢᴇᴛ_ᴘʀᴏxʏ_ꜰᴏʀ_ʟᴏᴄᴀᴛɪᴏɴ(target_location, task_id)  
            if not proxy_meta:  
                return None  
              
            # إنشاء اتصال SSL متقدم  
            ssl_context = ssl.create_default_context(cafile=certifi.where())  
            ssl_context.minimum_version = __ᴄᴏɴғɪɢ.ᴛʟs_ᴠᴇʀsɪᴏɴ  
            ssl_context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20')  
              
            # إنشاء موصل مع إعدادات متقدمة  
            connector = aiohttp.TCPConnector(  
                ssl=ssl_context,  
                enable_cleanup_closed=True,  
                force_close=False,  
                limit_per_host=0,  
                keepalive_timeout=30,  
                ttl_dns_cache=300  
            )  
              
            proxy_url = f"{proxy_meta.ᴛʏᴘᴇ.value}://{proxy_meta.ɪᴘ}:{proxy_meta.ᴘᴏʀᴛ}"  
              
            # توليد عناوين فريدة بناءً على موقع البروكسي  
            headers = self.ʜᴇᴀᴅᴇʀ_ɢᴇɴ.ɢᴇɴᴇʀᴀᴛᴇ_ʜᴇᴀᴅᴇʀs(proxy_meta.ɢᴇᴏ.ᴄᴏᴜɴᴛʀʏ)  
              
            # إعداد مهلة ذكية  
            timeout = aiohttp.ClientTimeout(  
                total=__ᴄᴏɴғɪɢ.ᴛɪᴍᴇᴏᴜᴛ_ᴘʀɪᴍᴀʀʏ,  
                connect=5,  
                sock_read=5,  
                sock_connect=5  
            )  
              
            # إنشاء الجلسة  
            session = aiohttp.ClientSession(  
                connector=connector,  
                timeout=timeout,  
                headers=headers  
            )  
              
            # تخزين البيانات الوصفية في الجلسة  
            session.proxy_meta = proxy_meta  
            session.task_id = task_id  
              
            self.ʟᴏɢɢᴇʀ.debug(f"Created client with proxy {proxy_meta.ᴜɴɪǫᴜᴇ_ɪᴅ} for task {task_id}")  
            return session  
              
        except Exception as e:  
            self.ʟᴏɢɢᴇʀ.error(f"Error creating proxy client: {e}")  
            return None  
      
    async def sᴀꜰᴇ_ʀᴇǫᴜᴇsᴛ(self, method: str, url: str, target_location: __ɢᴇᴏ_ʟᴏᴄᴀᴛɪᴏɴ,  
                            task_id: Optional[str] = None, **kwargs) -> Optional[aiohttp.ClientResponse]:  
        """طلب آمن مع استرجاع تلقائي للبروكسي"""  
        for attempt in range(__ᴄᴏɴғɪɢ.ᴍᴀx_ʀᴇᴛʀɪᴇs):  
            try:  
                session = await self.ᴄʀᴇᴀᴛᴇ_ᴘʀᴏxʏ_ᴄʟɪᴇɴᴛ(target_location, task_id)  
                if not session:  
                    continue  
                  
                async with session:  
                    response = await session.request(method, url, **kwargs)  
                      
                    if response.status in [200, 201, 202]:  
                        # تسجيل النجاح  
                        if hasattr(session, 'proxy_meta'):  
                            proxy_meta = session.proxy_meta  
                            proxy_meta.sᴜᴄᴄᴇss_ʀᴀᴛᴇ = min(1.0, proxy_meta.sᴜᴄᴄᴇss_ʀᴀᴛᴇ + 0.05)  
                          
                        return response  
                    else:  
                        # تسجيل الفشل  
                        if hasattr(session, 'proxy_meta'):  
                            await self.ʀᴇᴘᴏʀᴛ_ᴘʀᴏxʏ_ꜰᴀɪʟᴜʀᴇ(  
                                session.proxy_meta.ᴜɴɪǫᴜᴇ_ɪᴅ,  
                                f"HTTP {response.status}"  
                            )  
                  
            except aiohttp.ClientError as e:  
                if attempt < __ᴄᴏɴғɪɢ.ᴍᴀx_ʀᴇᴛʀɪᴇs - 1:  
                    # تدوير البروكسي لهذه المهمة  
                    if task_id and task_id in self.sᴛɪᴄᴋʏ_ᴛᴀsᴋs:  
                        self.__ʀᴏᴛᴀᴛᴇ_ᴛᴀsᴋ_ᴘʀᴏxʏ(task_id)  
                    await asyncio.sleep(1 * (attempt + 1))  
                else:  
                    self.ʟᴏɢɢᴇʀ.error(f"Request failed after {__ᴄᴏɴғɪɢ.ᴍᴀx_ʀᴇᴛʀɪᴇs} attempts: {e}")  
              
            except Exception as e:  
                self.ʟᴏɢɢᴇʀ.error(f"Unexpected error in safe_request: {e}")  
                break  
          
        return None  
      
    async def sᴛᴏᴘ(self):  
        """إيقاف النظام"""  
        self.ʟᴏɢɢᴇʀ.info("🛑 Stopping Geo-Proxy Orchestrator")  
        self.ʀᴜɴɴɪɴɢ = False  
          
        # تنظيف الموارد  
        self.ᴀᴄᴛɪᴠᴇ_ᴘʀᴏxɪᴇs.clear()  
        self.ɢᴇᴏ_ɪɴᴅᴇx.clear()  
        self.sᴛɪᴄᴋʏ_ᴛᴀsᴋs.clear()  
  
# ========== CAR  
ماهذا؟
