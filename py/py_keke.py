# -*- coding: utf-8 -*-
# @Author  : Doubebly (converted)
# @Time    : 2025/11/19
# TVBox-compatible rewrite of provided keke7 spider

import sys
import time
import json
import re
from urllib.parse import urlencode, urljoin
import requests
from lxml import etree
from bs4 import BeautifulSoup

sys.path.append('..')
from base.spider import Spider as BaseSpider


class Spider(BaseSpider):
    def getName(self):
        return "可可影视 (TVBox)"

    def init(self, extend):
        self.home_url = 'https://www.keke7.app'
        self.api_base = urljoin(self.home_url, '/api.php/provide/vod/')
        self.search_api = urljoin(self.home_url, '/index.php/ajax/suggest')
        self.image_domain = 'https://vres.cfaqcgj.com'
        self.default_play_url = 'https://sf1-cdn-tos.huoshanstatic.com/obj/media-fe/xgplayer_doc_video/mp4/xgplayer-demo-720p.mp4'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; TV) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36',
            'Referer': self.home_url + '/',
        }

        # requests session with simple retry
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=2)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def getDependence(self):
        return []

    def isVideoFormat(self, url):
        return isinstance(url, str) and url.endswith(('.mp4', '.m3u8', '.flv', '.ts'))

    def manualVideoCheck(self):
        return False

    def _get(self, url, params=None, json_resp=False, timeout=10):
        try:
            if params:
                url = url + ('&' if '?' in url else '?') + urlencode(params)
            r = self.session.get(url, headers=self.headers, timeout=timeout)
            r.raise_for_status()
            if json_resp:
                return r.json()
            return r.text
        except Exception as e:
            # simple fallback empty
            print(f"_get error: {e} url={url}")
            return None

    def getTimeToken(self):
        # try direct page parse for input[name=t]
        try:
            html = self._get(self.home_url)
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                t_input = soup.find('input', attrs={'name': 't'})
                if t_input and t_input.get('value'):
                    return re.sub(r'==$', '%3D%3D', t_input.get('value'))
        except Exception:
            pass
        return ''

    def homeContent(self, filter):
        classes = [
            {'type_id': '1', 'type_name': '电影'},
            {'type_id': '2', 'type_name': '剧集'},
            {'type_id': '4', 'type_name': '综艺'},
            {'type_id': '3', 'type_name': '动漫'},
            {'type_id': '6', 'type_name': '短剧'}
        ]

        # keep filters compact (same as original, but can be extended)
        filters = {
                '1': [
                    {'name': '剧情', 'key': 'class', 'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '剧情', 'v': '剧情'},
                        {'n': '喜剧', 'v': '喜剧'},
                        {'n': '动作', 'v': '动作'},
                        {'n': '爱情', 'v': '爱情'},
                        {'n': '恐怖', 'v': '恐怖'},
                        {'n': '惊悚', 'v': '惊悚'},
                        {'n': '犯罪', 'v': '犯罪'},
                        {'n': '科幻', 'v': '科幻'},
                        {'n': '悬疑', 'v': '悬疑'},
                        {'n': '奇幻', 'v': '奇幻'},
                        {'n': '冒险', 'v': '冒险'},
                        {'n': '战争', 'v': '战争'},
                        {'n': '历史', 'v': '历史'},
                        {'n': '古装', 'v': '古装'},
                        {'n': '家庭', 'v': '家庭'},
                        {'n': '武侠', 'v': '武侠'},
                        {'n': '歌舞', 'v': '歌舞'},
                        {'n': '动画', 'v': '动画'}]},
                    {'name': '地区', 'key': 'area', 'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '台湾', 'v': '中国台湾'},
                        {'n': '日本', 'v': '日本'},
                        {'n': '韩国', 'v': '韩国'},
                        {'n': '美国', 'v': '美国'},
                        {'n': '英国', 'v': '英国'},
                        {'n': '大陆', 'v': '中国大陆'},
                        {'n': '香港', 'v': '中国香港'},
                        {'n': '法国', 'v': '法国'}]},
                    {'name': '语言', 'key': 'lang', 'value': [  # 新增語言篩選
                        {'n': '全部', 'v': ''},
                        {'n': '国语', 'v': '国语'},
                        {'n': '英语', 'v': '英语'},
                        {'n': '粤语', 'v': '粤语'},
                        {'n': '日语', 'v': '日语'},
                        {'n': '韩语', 'v': '韩语'}
                    ]},
                    {'name': '年份', 'key': 'year', 'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '2025', 'v': '2025'},
                        {'n': '2024', 'v': '2024'},
                        {'n': '2023', 'v': '2023'},
                        {'n': '2022', 'v': '2022'},
                        {'n': '2021', 'v': '2021'},
                        {'n': '2020', 'v': '2020'},
                        {'n': '10年代', 'v': '2010_2019'},
                        {'n': '00年代', 'v': '2000_2009'},
                        {'n': '90年代', 'v': '1990_1999'},
                        {'n': '80年代', 'v': '1980_1989'},
                        {'n': '更早', 'v': '0_1979'}
                    ]},
                    {'name': '排序', 'key': 'by', 'value': [
                        {'n': '綜合排序', 'v': '1'},
                        {'n': '按時間', 'v': '2'},
                        {'n': '按熱度', 'v': '3'},
                        {'n': '按評分', 'v': '4'}
                    ]}
                ],
                '2': [
                    {'name': '剧情', 'key': 'class', 'value': [
                        {'n': '全部', 'v': ''},
                        {'n': 'Netflix', 'v': 'Netflix'},
                        {'n': '剧情', 'v': '剧情'},
                        {'n': '爱情', 'v': '爱情'},
                        {'n': '喜剧', 'v': '喜剧'},
                        {'n': '犯罪', 'v': '犯罪'},
                        {'n': '悬疑', 'v': '悬疑'},
                        {'n': '古装', 'v': '古装'},
                        {'n': '动作', 'v': '动作'},
                        {'n': '家庭', 'v': '家庭'},
                        {'n': '惊悚', 'v': '惊悚'},
                        {'n': '奇幻', 'v': '奇幻'},
                        {'n': '美剧', 'v': '美剧'},
                        {'n': '韩剧', 'v': '韩剧'},
                        {'n': '科幻', 'v': '科幻'},
                        {'n': '历史', 'v': '历史'},
                        {'n': '战争', 'v': '战争'},
                        {'n': '武侠', 'v': '武侠'},
                        {'n': '言情', 'v': '言情'},
                        {'n': '恐怖', 'v': '恐怖'},
                        {'n': '冒险', 'v': '冒险'},
                        {'n': '都市', 'v': '都市'},
                        {'n': '职场', 'v': '职场'}]},
                    {'name': '地区', 'key': 'area', 'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '台湾', 'v': '中国台湾'},
                        {'n': '日本', 'v': '日本'},
                        {'n': '韩国', 'v': '韩国'},
                        {'n': '美国', 'v': '美国'},
                        {'n': '英国', 'v': '英国'},
                        {'n': '大陆', 'v': '中国大陆'},
                        {'n': '香港', 'v': '中国香港'},
                        {'n': '法国', 'v': '法国'}]},
                    {'name': '语言', 'key': 'lang', 'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '国语', 'v': '国语'},
                        {'n': '英语', 'v': '英语'},
                        {'n': '粤语', 'v': '粤语'},
                        {'n': '日语', 'v': '日语'},
                        {'n': '韩语', 'v': '韩语'}
                    ]},
                    {'name': '年份', 'key': 'year', 'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '2025', 'v': '2025'},
                        {'n': '2024', 'v': '2024'},
                        {'n': '2023', 'v': '2023'},
                        {'n': '2022', 'v': '2022'},
                        {'n': '2021', 'v': '2021'},
                        {'n': '2020', 'v': '2020'},
                        {'n': '10年代', 'v': '2010_2019'},
                        {'n': '00年代', 'v': '2000_2009'},
                        {'n': '90年代', 'v': '1990_1999'},
                        {'n': '80年代', 'v': '1980_1989'},
                        {'n': '更早', 'v': '0_1979'}
                    ]},
                    {'name': '排序', 'key': 'by', 'value': [
                        {'n': '綜合排序', 'v': '1'},
                        {'n': '按時間', 'v': '2'},
                        {'n': '按熱度', 'v': '3'},
                        {'n': '按評分', 'v': '4'}
                    ]}
                ],
                '3': [
                    {'name': '剧情', 'key': 'class', 'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '动态漫画', 'v': '动态漫画'},
                        {'n': '剧情', 'v': '剧情'},
                        {'n': '动画', 'v': '动画'},
                        {'n': '喜剧', 'v': '喜剧'},
                        {'n': '冒险', 'v': '冒险'},
                        {'n': '动作', 'v': '动作'},
                        {'n': '奇幻', 'v': '奇幻'},
                        {'n': '科幻', 'v': '科幻'},
                        {'n': '儿童', 'v': '儿童'},
                        {'n': '搞笑', 'v': '搞笑'},
                        {'n': '爱情', 'v': '爱情'},
                        {'n': '家庭', 'v': '家庭'},
                        {'n': '短片', 'v': '短片'},
                        {'n': '热血', 'v': '热血'},
                        {'n': '益智', 'v': '益智'},
                        {'n': '悬疑', 'v': '悬疑'},
                        {'n': '经典', 'v': '经典'},
                        {'n': '校园', 'v': '校园'},
                        {'n': 'Anime', 'v': 'Anime'},
                        {'n': '运动', 'v': '运动'},
                        {'n': '亲子', 'v': '亲子'},
                        {'n': '青春', 'v': '青春'},
                        {'n': '恋爱', 'v': '恋爱'},
                        {'n': '武侠', 'v': '武侠'},
                        {'n': '惊悚', 'v': '惊悚'}]},
                    {'name': '地区', 'key': 'area', 'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '大陆', 'v': '中国大陆'},
                        {'n': '香港', 'v': '中国香港'},
                        {'n': '台湾', 'v': '中国台湾'},
                        {'n': '美国', 'v': '美国'},
                        {'n': '日本', 'v': '日本'},
                        {'n': '韩国', 'v': '韩国'},
                        {'n': '英国', 'v': '英国'},
                        {'n': '法国', 'v': '法国'}]},
                    {'name': '语言', 'key': 'lang', 'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '国语', 'v': '国语'},
                        {'n': '英语', 'v': '英语'},
                        {'n': '粤语', 'v': '粤语'},
                        {'n': '日语', 'v': '日语'},
                        {'n': '韩语', 'v': '韩语'}
                    ]},
                    {'name': '年份', 'key': 'year', 'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '2025', 'v': '2025'},
                        {'n': '2024', 'v': '2024'},
                        {'n': '2023', 'v': '2023'},
                        {'n': '2022', 'v': '2022'},
                        {'n': '2021', 'v': '2021'},
                        {'n': '2020', 'v': '2020'},
                        {'n': '10年代', 'v': '2010_2019'},
                        {'n': '00年代', 'v': '2000_2009'},
                        {'n': '90年代', 'v': '1990_1999'},
                        {'n': '80年代', 'v': '1980_1989'},
                        {'n': '更早', 'v': '0_1979'}
                    ]},
                    {'name': '排序', 'key': 'by', 'value': [
                        {'n': '綜合排序', 'v': '1'},
                        {'n': '按時間', 'v': '2'},
                        {'n': '按熱度', 'v': '3'},
                        {'n': '按評分', 'v': '4'}
                    ]}
                ],
                '4': [
                    {'name': '剧情', 'key': 'class', 'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '纪录', 'v': '纪录'},
                        {'n': '真人秀', 'v': '真人秀'},
                        {'n': '脱口秀', 'v': '脱口秀'},
                        {'n': '剧情', 'v': '剧情'},
                        {'n': '历史', 'v': '历史'},
                        {'n': '喜剧', 'v': '喜剧'},
                        {'n': '传记', 'v': '传记'},
                        {'n': '相声', 'v': '相声'},
                        {'n': '节目', 'v': '节目'},
                        {'n': '运动', 'v': '运动'},
                        {'n': '犯罪', 'v': '犯罪'},
                        {'n': '短片', 'v': '短片'},
                        {'n': '搞笑', 'v': '搞笑'},
                        {'n': '晚会', 'v': '晚会'}]},
                    {'name': '地区', 'key': 'area', 'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '台湾', 'v': '中国台湾'},
                        {'n': '日本', 'v': '日本'},
                        {'n': '韩国', 'v': '韩国'},
                        {'n': '美国', 'v': '美国'},
                        {'n': '英国', 'v': '英国'},
                        {'n': '大陆', 'v': '中国大陆'},
                        {'n': '香港', 'v': '中国香港'},
                        {'n': '法国', 'v': '法国'}]},
                    {'name': '语言', 'key': 'lang', 'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '国语', 'v': '国语'},
                        {'n': '英语', 'v': '英语'},
                        {'n': '粤语', 'v': '粤语'},
                        {'n': '日语', 'v': '日语'},
                        {'n': '韩语', 'v': '韩语'}
                    ]},
                    {'name': '年份', 'key': 'year', 'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '2025', 'v': '2025'},
                        {'n': '2024', 'v': '2024'},
                        {'n': '2023', 'v': '2023'},
                        {'n': '2022', 'v': '2022'},
                        {'n': '2021', 'v': '2021'},
                        {'n': '2020', 'v': '2020'},
                        {'n': '10年代', 'v': '2010_2019'},
                        {'n': '00年代', 'v': '2000_2009'},
                        {'n': '90年代', 'v': '1990_1999'},
                        {'n': '80年代', 'v': '1980_1989'},
                        {'n': '更早', 'v': '0_1979'}
                    ]},
                    {'name': '排序', 'key': 'by', 'value': [
                        {'n': '綜合排序', 'v': '1'},
                        {'n': '按時間', 'v': '2'},
                        {'n': '按熱度', 'v': '3'},
                        {'n': '按評分', 'v': '4'}
                    ]}
                ],
                '6': [
                    {'name': '剧情', 'key': 'class', 'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '逆袭', 'v': '逆袭'},
                        {'n': '甜宠', 'v': '甜宠'},
                        {'n': '虐恋', 'v': '虐恋'},
                        {'n': '穿越', 'v': '穿越'},
                        {'n': '重生', 'v': '重生'},
                        {'n': '剧情', 'v': '剧情'},
                        {'n': '科幻', 'v': '科幻'},
                        {'n': '武侠', 'v': '武侠'},
                        {'n': '动作', 'v': '动作'},
                        {'n': '爱情', 'v': '爱情'},
                        {'n': '战争', 'v': '战争'},
                        {'n': '冒险', 'v': '冒险'},
                        {'n': '其它', 'v': '其它'}]},
                    {'name': '排序', 'key': 'by', 'value': [
                        {'n': '綜合排序', 'v': '1'},
                        {'n': '按時間', 'v': '2'},
                        {'n': '按熱度', 'v': '3'},
                        {'n': '按評分', 'v': '4'}
                    ]}
                ]
            }

        return {'class': classes, 'filters': filters}

    def homeVideoContent(self):
        # try API first for latest
        params = {'ac': 'list', 't': 1, 'pg': 1}
        api_url = self.api_base + '?' + urlencode(params)
        try:
            data = self._get(api_url, json_resp=True)
            if data and isinstance(data, dict) and data.get('list'):
                items = []
                for v in data.get('list'):
                    items.append({
                        'vod_id': v.get('vod_id'),
                        'vod_name': v.get('vod_name'),
                        'vod_pic': v.get('vod_pic') if v.get('vod_pic', '').startswith('http') else (self.image_domain.rstrip('/') + '/' + v.get('vod_pic','').lstrip('/')),
                        'vod_remarks': v.get('vod_remarks', '')
                    })
                return {'list': items, 'parse': 0, 'jx': 0}
        except Exception:
            pass

        # fallback to HTML scraping
        d = []
        html = self._get(self.home_url)
        if not html:
            return {'list': d, 'parse': 0, 'jx': 0}
        root = etree.HTML(html)
        nodes = root.xpath('//div[contains(@class,"module-item")]//a[contains(@class,"v-item")]')
        for i in nodes:
            href = (i.xpath('./@href') or [''])[0]
            name = ''.join(i.xpath('.//div[contains(@class,"v-item-title")]/text()') or ['']).strip()
            pic = (i.xpath('.//img/@data-original') or i.xpath('.//img/@src') or [''])[0]
            if pic and not pic.startswith('http'):
                pic = self.image_domain.rstrip('/') + '/' + pic.lstrip('/')
            remarks = ''.join(i.xpath('.//div[contains(@class,"v-item-bottom")]//span/text()') or ['']).strip()
            if href or name:
                d.append({'vod_id': href, 'vod_name': name, 'vod_pic': pic, 'vod_remarks': remarks})
        return {'list': d, 'parse': 0, 'jx': 0}

    def categoryContent(self, cid, page, filter, ext):
        # prefer API when possible
        params = {'ac': 'detail', 't': cid, 'pg': page}
        if ext:
            if ext.get('class'): params['class'] = ext.get('class')
            if ext.get('area'): params['area'] = ext.get('area')
            if ext.get('lang'): params['lang'] = ext.get('lang')
            if ext.get('year'): params['year'] = ext.get('year')
            if ext.get('by'): params['by'] = ext.get('by')
        api_url = self.api_base + '?' + urlencode(params)
        data = self._get(api_url, json_resp=True)
        d = []
        if data and isinstance(data, dict) and data.get('list'):
            for v in data.get('list', []):
                pic = v.get('vod_pic','')
                if pic and not pic.startswith('http'):
                    pic = self.image_domain.rstrip('/') + '/' + pic.lstrip('/')
                d.append({'vod_id': v.get('vod_id'), 'vod_name': v.get('vod_name'), 'vod_pic': pic, 'vod_remarks': v.get('vod_remarks','')})
            return {'list': d, 'parse': 0, 'jx': 0}

        # fallback HTML
        url = self.home_url + f'/show/{cid}-{ext.get("class","")}-{ext.get("area","")}-{ext.get("lang","")}-{ext.get("year","")}-{ext.get("by","")}-{page}.html'
        html = self._get(url)
        if not html:
            return {'list': d, 'parse': 0, 'jx': 0}
        root = etree.HTML(html)
        nodes = root.xpath('//div[contains(@class,"module-item")]//a[contains(@class,"v-item")]')
        for i in nodes:
            href = (i.xpath('./@href') or [''])[0]
            name = ''.join(i.xpath('.//div[contains(@class,"v-item-title")]/text()') or ['']).strip()
            pic = (i.xpath('.//img/@data-original') or i.xpath('.//img/@src') or [''])[0]
            if pic and not pic.startswith('http'):
                pic = self.image_domain.rstrip('/') + '/' + pic.lstrip('/')
            remarks = ''.join(i.xpath('.//div[contains(@class,"v-item-bottom")]//span/text()') or ['']).strip()
            d.append({'vod_id': href, 'vod_name': name, 'vod_pic': pic, 'vod_remarks': remarks})
        return {'list': d, 'parse': 0, 'jx': 0}

    def detailContent(self, did):
        ids = did[0] if isinstance(did, (list, tuple)) else did
        if not ids:
            return {'list': [], 'parse': 0, 'jx': 0}

        # try API detail first
        api_url = self.api_base + '?ac=detail&ids=' + str(ids)
        data = self._get(api_url, json_resp=True)
        if data and isinstance(data, dict) and data.get('list'):
            v = data['list'][0]
            # normalize pic
            pic = v.get('vod_pic','')
            if pic and not pic.startswith('http'):
                pic = self.image_domain.rstrip('/') + '/' + pic.lstrip('/')

            # split play sources
            play_from = v.get('vod_play_from','')
            play_url = v.get('vod_play_url','')
            play_from_list = play_from.split('$$$') if play_from else []
            play_url_list = play_url.split('$$$') if play_url else []

            # ensure absolute urls in play lists
            fixed_play_url_list = []
            for group in play_url_list:
                entries = group.split('#') if group else []
                fixed = []
                for e in entries:
                    if '$' in e:
                        name, u = e.split('$',1)
                        if not u.startswith('http'):
                            u = urljoin(self.home_url, u)
                        fixed.append(f"{name}${u}")
                fixed_play_url_list.append('#'.join(fixed))

            vod = {
                'type_name': v.get('type_name',''),
                'vod_id': v.get('vod_id',''),
                'vod_name': v.get('vod_name',''),
                'vod_remarks': v.get('vod_remarks',''),
                'vod_year': v.get('vod_year',''),
                'vod_area': v.get('vod_area',''),
                'vod_actor': v.get('vod_actor',''),
                'vod_director': v.get('vod_director',''),
                'vod_content': v.get('vod_content',''),
                'vod_play_from': '$$$'.join(play_from_list),
                'vod_play_url': '$$$'.join(fixed_play_url_list)
            }
            return {'list': [vod], 'parse': 0, 'jx': 0}

        # fallback to HTML parsing
        url = self.home_url + ids if ids.startswith('/') else (self.home_url + '/' + ids)
        html = self._get(url)
        if not html:
            return {'list': [], 'parse': 0, 'jx': 0}
        root = etree.HTML(html)

        vod_play_from_list = root.xpath('//span[contains(@class,"source-item-label")]/text()')
        vod_play_from = '$$$'.join([x.strip() for x in vod_play_from_list if x.strip()])
        play_nodes = root.xpath('//div[contains(@class,"episode-list")]')
        vod_play_url_list = []
        for node in play_nodes:
            names = [n.strip() for n in node.xpath('./a/text()') if n.strip()]
            urls = [u.strip() for u in node.xpath('./a/@href') if u.strip()]
            pairs = []
            for _n, _u in zip(names, urls):
                u_final = _u if _u.startswith('http') else urljoin(self.home_url, _u)
                pairs.append(f"{_n}${u_final}")
            if pairs:
                vod_play_url_list.append('#'.join(pairs))
        vod_play_url = '$$$'.join(vod_play_url_list)

        vod = {
            'type_name': '',
            'vod_id': ids,
            'vod_name': (root.xpath('//h1/text()') or [''])[0].strip(),
            'vod_remarks': '',
            'vod_year': (root.xpath('//span[contains(@class,"year")]/text()') or [''])[0].strip(),
            'vod_area': (root.xpath('//span[contains(@class,"area")]/text()') or [''])[0].strip(),
            'vod_actor': ''.join(root.xpath('//div[contains(@class,"actor")]//text()') or []).strip(),
            'vod_director': ''.join(root.xpath('//div[contains(@class,"director")]//text()') or []).strip(),
            'vod_content': ''.join(root.xpath('//div[contains(@class,"video-desc")]//text()') or []).strip(),
            'vod_play_from': vod_play_from,
            'vod_play_url': vod_play_url
        }
        return {'list': [vod], 'parse': 0, 'jx': 0}

    def searchContent(self, key, quick, page='1'):
        # try search API
        params = {'mid': 1, 'wd': key}
        try:
            data = self._get(self.search_api, params=params, json_resp=True)
            results = []
            if data and isinstance(data, dict) and data.get('list'):
                for v in data.get('list'):
                    pic = v.get('pic','')
                    if pic and not pic.startswith('http'):
                        pic = self.image_domain.rstrip('/') + '/' + pic.lstrip('/')
                    results.append({'vod_id': v.get('id'), 'vod_name': v.get('name'), 'vod_pic': pic, 'vod_remarks': v.get('actor','')})
                return {'list': results, 'parse': 0, 'jx': 0}
        except Exception:
            pass

        # fallback to page search
        token = self.getTimeToken()
        url = f"{self.home_url}/search?k={key}"
        if token:
            url += f"&t={token}"
        html = self._get(url)
        results = []
        if not html:
            return {'list': results, 'parse': 0, 'jx': 0}
        root = etree.HTML(html)
        nodes = root.xpath('//a[contains(@class,"search-result-item")]')
        for i in nodes:
            href = (i.xpath('./@href') or [''])[0]
            name = (i.xpath('.//div[contains(@class,"title")]/text()') or [''])[0].strip()
            pic = (i.xpath('.//img/@data-original') or i.xpath('.//img/@src') or [''])[0]
            if pic and not pic.startswith('http'):
                pic = self.image_domain.rstrip('/') + '/' + pic.lstrip('/')
            remark = (i.xpath('.//div[contains(@class,"tags")]/span[1]/text()') or [''])[0]
            results.append({'vod_id': href, 'vod_name': name, 'vod_pic': pic, 'vod_remarks': remark})
        return {'list': results, 'parse': 0, 'jx': 0}

    def playerContent(self, flag, pid, vipFlags):
        # pid may be path or full url
        url = pid if pid.startswith('http') else (self.home_url + pid if pid.startswith('/') else (self.home_url + '/' + pid))
        try:
            html = self._get(url)
            if not html:
                return {'url': url, 'parse': 1, 'jx': 0}

            # try to find direct sources in JS
            m = re.search(r'src\s*[:=]\s*"(https?://[^"]+?)"', html)
            if m:
                return {'url': m.group(1), 'parse': 0, 'jx': 0, 'header': {'User-Agent': 'okhttp/5.0.0'}}

            # try video/source tags
            root = etree.HTML(html)
            src = (root.xpath('//video/source/@src') or root.xpath('//video/@src') or root.xpath('//iframe/@src') or [])
            if src:
                s = src[0]
                if not s.startswith('http'):
                    s = urljoin(self.home_url, s)
                return {'url': s, 'parse': 0, 'jx': 0, 'header': {'User-Agent': 'okhttp/5.0.0'}}

            # no direct url -> return to player sniffing
            return {'url': url, 'parse': 1, 'jx': 0}
        except Exception as e:
            print(f"playerContent error: {e}")
            return {'url': self.default_play_url, 'parse': 0, 'jx': 0}

    def localProxy(self, params):
        return None

    def destroy(self):
        try:
            self.session.close()
        except:
            pass
        return '正在Destroy'


if __name__ == '__main__':
    pass
