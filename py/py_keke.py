# -*- coding: utf-8 -*-
# @Author  : Doubebly (fixed)
# @Time    : 2025/11/19  (fixed)

import sys
import re
import time
import requests
from lxml import etree
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

sys.path.append('..')
from base.spider import Spider as BaseSpider  # avoid name clash

class Spider(BaseSpider):
    def getName(self):
        return "可可影视"

    def init(self, extend):
        self.home_url = 'https://www.keke7.app'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
            "Referer": self.home_url + "/",
        }
        self.image_domain = "https://vres.cfaqcgj.com"  # 圖片域名（若圖片為相對路徑則組合）
        self.default_play_url = 'https://sf1-cdn-tos.huoshanstatic.com/obj/media-fe/xgplayer_doc_video/mp4/xgplayer-demo-720p.mp4'
        # optional: timeout (ms) for playwright navigation
        self.playwright_timeout = 60000

    def getDependence(self):
        return []

    def isVideoFormat(self, url):
        # 可自行擴充判斷影片格式
        return url.endswith(('.mp4', '.m3u8', '.flv', '.ts'))

    def manualVideoCheck(self):
        return False

    # ---- helper: 使用 Playwright 取得渲染後的 HTML ----
    def _fetch_html_with_playwright(self, url, wait_selector=None):
        """
        使用 Playwright 抓取渲染後 HTML，若 wait_selector 提供則會等待該 selector 出現（最多 self.playwright_timeout ms）
        返回 str html（或 '' 若發生錯誤）
        """
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
                context = browser.new_context(user_agent=self.headers["User-Agent"])
                page = context.new_page()
                page.goto(url, timeout=self.playwright_timeout)
                if wait_selector:
                    try:
                        page.wait_for_selector(wait_selector, timeout=self.playwright_timeout)
                    except PlaywrightTimeoutError:
                        # not fatal — 可能頁面沒有該 selector
                        pass
                html = page.content()
                browser.close()
                return html
        except Exception as e:
            print(f"_fetch_html_with_playwright error: {e}")
            return ''

    # ---- 取得 token 的備援方法（先用 requests 嘗試，再用 playwright） ----
    def getTimeToken(self):
        try:
            res = requests.get(self.home_url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(res.content, 'html.parser')
            t_input = soup.find('input', attrs={'name': 't'})
            if t_input and t_input.get('value'):
                return re.sub(r'==$', '%3D%3D', t_input.get('value'))
        except Exception:
            pass

        # fallback: 用 playwright 渲染取得
        html = self._fetch_html_with_playwright(self.home_url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            t_input = soup.find('input', attrs={'name': 't'})
            if t_input and t_input.get('value'):
                return re.sub(r'==$', '%3D%3D', t_input.get('value'))
        return ''

    # ---- homeContent (靜態分類資訊) ----
    def homeContent(self, filter):
    result = {
        'class': [
            {'type_id': '1', 'type_name': '电影'},
            {'type_id': '2', 'type_name': '剧集'},
            {'type_id': '4', 'type_name': '综艺'},
            {'type_id': '3', 'type_name': '动漫'},
            {'type_id': '6', 'type_name': '短剧'}
        ],
        'filters': {
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
    }
    print(f"Debug homeContent: {result}")
    return result

    # ---- homeVideoContent: 使用 Playwright 抓取首頁的動態內容 ----
    def homeVideoContent(self):
        d = []
        try:
            html = self._fetch_html_with_playwright(self.home_url, wait_selector="div.module-item a.v-item")
            if not html:
                return {"list": d, "parse": 0, "jx": 0}

            root = etree.HTML(html)
            items = root.xpath('//div[contains(@class,"module-item")]//a[contains(@class,"v-item")]')
            for i in items:
                # href 可能是完整或相對路徑
                hrefs = i.xpath('./@href')
                vod_id = hrefs[0] if hrefs else ''
                title_list = i.xpath('.//div[contains(@class,"v-item-title")]/text()')
                # 允許圖片在 src 或 data-original
                pic = i.xpath('.//img/@data-original') or i.xpath('.//img/@src') or ['']
                remarks = ''.join(i.xpath('.//div[contains(@class,"v-item-bottom")]//span/text()')).strip()
                vod_name = title_list[0].strip() if title_list else ''
                vod_pic = pic[0].strip() if pic and pic[0] else ''
                if vod_pic and not vod_pic.startswith('http'):
                    vod_pic = self.image_domain.rstrip('/') + '/' + vod_pic.lstrip('/')

                if not vod_id and vod_name == '':
                    continue

                d.append({
                    "vod_id": vod_id,
                    "vod_name": vod_name,
                    "vod_pic": vod_pic,
                    "vod_remarks": remarks
                })
            return {"list": d, "parse": 0, "jx": 0}
        except Exception as e:
            print("爬蟲錯誤 homeVideoContent：", e)
            return {"list": [], "parse": 0, "jx": 0}

    # ---- categoryContent: 分類頁也用 Playwright（因為是動態） ----
    def categoryContent(self, cid, page, filter, ext):
        _class = ext.get('class', '')
        _area = ext.get('area', '')
        _language = ext.get('lang', '')
        _year = ext.get('year', '')
        _by = ext.get('by', '')

        url = self.home_url + f'/show/{cid}-{_class}-{_area}-{_language}-{_year}-{_by}-{page}.html'
        d = []
        try:
            html = self._fetch_html_with_playwright(url, wait_selector='div.module-item a.v-item')
            if not html:
                return {'list': d, 'parse': 0, 'jx': 0}

            root = etree.HTML(html)
            data_list = root.xpath('//div[contains(@class,"module-box-inner")]//div[contains(@class,"module-item")]//a[contains(@class,"v-item")]')
            for i in data_list:
                vod_id = (i.xpath('./@href') or [''])[0]
                vod_name_list = i.xpath('.//div[contains(@class,"v-item-title")]/text()')
                vod_name = vod_name_list[0].strip() if vod_name_list else ''
                pic_list = i.xpath('.//img/@data-original') or i.xpath('.//img/@src') or ['']
                vod_pic = pic_list[0].strip() if pic_list and pic_list[0] else ''
                if vod_pic and not vod_pic.startswith('http'):
                    vod_pic = self.image_domain.rstrip('/') + '/' + vod_pic.lstrip('/')
                vod_remarks = ''.join(i.xpath('.//div[contains(@class,"v-item-bottom")]//span/text()')).strip()
                d.append({
                    'vod_id': vod_id,
                    'vod_name': vod_name,
                    'vod_pic': vod_pic,
                    'vod_remarks': vod_remarks
                })
            return {'list': d, 'parse': 0, 'jx': 0}
        except Exception as e:
            print("categoryContent error:", e)
            return {'list': d, 'parse': 0, 'jx': 0}

    # ---- detailContent: 影片詳情與播放清單 ----
    def detailContent(self, did):
        # did 可能是 ['/path/xxx.html'] 或類似
        ids = did[0] if isinstance(did, (list, tuple)) and len(did) > 0 else did
        video_list = []
        if not ids:
            return {'list': [], 'parse': 0, 'jx': 0}

        url = self.home_url + ids if ids.startswith('/') else self.home_url + '/' + ids
        try:
            html = self._fetch_html_with_playwright(url, wait_selector='div.episode-list')
            if not html:
                # fallback 使用 requests（若伺服器回傳靜態有用）
                res = requests.get(url, headers=self.headers, timeout=15)
                html = res.text

            root = etree.HTML(html)
            vod_play_from_list = root.xpath('//span[contains(@class,"source-item-label")]/text()')
            vod_play_from = '$$$'.join([x.strip() for x in vod_play_from_list if x.strip()])

            play_list_nodes = root.xpath('//div[contains(@class,"episode-list")]')
            vod_play_url_list = []
            for node in play_list_nodes:
                name_list = [n.strip() for n in node.xpath('./a/text()') if n.strip()]
                url_list = [u.strip() for u in node.xpath('./a/@href') if u.strip()]
                pairs = []
                for _n, _u in zip(name_list, url_list):
                    pairs.append(_n + '$' + _u)
                if pairs:
                    vod_play_url_list.append('#'.join(pairs))

            vod_play_url = '$$$'.join(vod_play_url_list)
            # 其它 metadata（盡量從 page 抓）
            vod_name = (root.xpath('//h1/text()') or [''])[0].strip()
            vod_content = ''.join(root.xpath('//div[contains(@class,"video-desc")]//text()')).strip() or ''
            vod_actor = ''.join(root.xpath('//div[contains(@class,"actor")]//text()')).strip() or ''
            vod_director = ''.join(root.xpath('//div[contains(@class,"director")]//text()')).strip() or ''

            video_list.append({
                'type_name': '',
                'vod_id': ids,
                'vod_name': vod_name,
                'vod_remarks': '',
                'vod_year': '',
                'vod_area': '',
                'vod_actor': vod_actor,
                'vod_director': vod_director,
                'vod_content': vod_content,
                'vod_play_from': vod_play_from,
                'vod_play_url': vod_play_url
            })
            return {"list": video_list, 'parse': 0, 'jx': 0}
        except Exception as e:
            print(f"Error in detailContent: {e}")
            return {'list': [], 'msg': str(e)}

    # ---- searchContent: 使用 token 並以 Playwright 抓取（若需要） ----
    def searchContent(self, key, quick, page='1'):
        token = self.getTimeToken()
        url = f'{self.home_url}/search?k={key}'
        if token:
            url = f'{self.home_url}/search?k={key}&t={token}'
        d = []
        try:
            # 試用 requests 先抓（較輕量），若回傳沒有結果再用 playwright
            res = requests.get(url, headers=self.headers, timeout=15)
            html = res.text if res.status_code == 200 else ''
            root = etree.HTML(html) if html else None
            data_list = root.xpath('//a[contains(@class,"search-result-item")]') if root is not None else []

            if not data_list:
                # fallback: playwright
                html = self._fetch_html_with_playwright(url, wait_selector='a.search-result-item')
                if not html:
                    return {'list': d, 'parse': 0, 'jx': 0}
                root = etree.HTML(html)
                data_list = root.xpath('//a[contains(@class,"search-result-item")]')

            for i in data_list:
                vod_id = (i.xpath('./@href') or [''])[0]
                vod_name = (i.xpath('.//div[contains(@class,"title")]/text()') or [''])[0].strip()
                pic = (i.xpath('.//img/@data-original') or i.xpath('.//img/@src') or [''])[0]
                if pic and not pic.startswith('http'):
                    pic = self.image_domain.rstrip('/') + '/' + pic.lstrip('/')
                vod_remarks = (i.xpath('.//div[contains(@class,"tags")]/span[1]/text()') or [''])[0].strip()
                d.append({
                    'vod_id': vod_id,
                    'vod_name': vod_name,
                    'vod_pic': pic,
                    'vod_remarks': vod_remarks
                })
            result = {'list': d, 'parse': 0, 'jx': 0}
            return result
        except Exception as e:
            print(f"Error in searchContent: {e}")
            return {'list': [], 'parse': 0, 'jx': 0}

    # ---- playerContent: 取得播放真實 URL 或回傳嗅探鏈接 ----
    def playerContent(self, flag, pid, vipFlags):
        # pid 可能為相對路徑或播放頁面
        url = self.home_url + pid if pid.startswith('/') else (pid if pid.startswith('http') else self.home_url + '/' + pid)
        try:
            # 使用 requests 先嘗試解析蘊含的 src 字串
            res = requests.get(url, headers=self.headers, timeout=15)
            text = res.text or ''
            # 嘗試直接找 JS 中的 src: "...",
            play_url_list = re.findall(r'src[:=]\s*"(https?://[^"]+)"', text)
            if not play_url_list:
                # 用 playwright 渲染後再找
                html = self._fetch_html_with_playwright(url, wait_selector='video, iframe, source')
                if html:
                    play_url_list = re.findall(r'src[:=]\s*"(https?://[^"]+)"', html)
                # 另外嘗試 iframe 或 video 標籤
                if not play_url_list and html:
                    root = etree.HTML(html)
                    # video source
                    src = (root.xpath('//video/source/@src') or root.xpath('//video/@src') or root.xpath('//iframe/@src') or []) 
                    if src:
                        play_url_list = src

            if play_url_list:
                play_url = play_url_list[0]
                # 若是 .m3u8 或 mp4，直接回傳，並包含必要 header（部份播放器需要）
                header = {"User-Agent": "okhttp/5.0.0"}
                return {'url': play_url, 'parse': 0, 'jx': 0, 'header': header}
            # 若都沒抓到，回傳嗅探連結給上層處理
            return {'url': url, 'parse': 1, 'jx': 0}
        except Exception as e:
            print(f"Error in playerContent: {e}")
            return {'url': self.default_play_url, 'parse': 0, 'jx': 0}

    def localProxy(self, params):
        # 如需實作本地轉 proxy，可在此擴充
        return None

    def destroy(self):
        return '正在Destroy'

if __name__ == '__main__':
    pass
