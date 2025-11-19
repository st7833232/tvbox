# -*- coding: utf-8 -*-
# @Author  : Doubebly (fixed)
# @Time    : 2025/11/19  (fixed)

import sys
import re
import requests
from lxml import etree
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

sys.path.append('..')
from base.spider import Spider as BaseSpider

class Spider(BaseSpider):
    def getName(self):
        return "可可影视"

    def init(self, extend):
        self.home_url = 'https://www.keke7.app'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
            "Referer": self.home_url + "/",
        }
        self.image_domain = "https://vres.cfaqcgj.com"
        self.default_play_url = 'https://sf1-cdn-tos.huoshanstatic.com/obj/media-fe/xgplayer_doc_video/mp4/xgplayer-demo-720p.mp4'
        self.playwright_timeout = 60000

    def getDependence(self):
        return []

    def isVideoFormat(self, url):
        return url.endswith(('.mp4', '.m3u8', '.flv', '.ts'))

    def manualVideoCheck(self):
        return False

    # ---- Playwright 瀏覽器管理 ----
    _playwright_browser = None
    _playwright_context = None

    def _init_playwright(self):
        if not self._playwright_browser:
            self._playwright = sync_playwright().start()
            self._playwright_browser = self._playwright.chromium.launch(headless=True, args=["--no-sandbox"])
            self._playwright_context = self._playwright_browser.new_context(user_agent=self.headers["User-Agent"])

    def _close_playwright(self):
        try:
            if self._playwright_context:
                self._playwright_context.close()
                self._playwright_context = None
            if self._playwright_browser:
                self._playwright_browser.close()
                self._playwright_browser = None
            if hasattr(self, '_playwright'):
                self._playwright.stop()
        except Exception as e:
            print(f"_close_playwright error: {e}")

    def _fetch_html_with_playwright(self, url, wait_selector=None):
        try:
            self._init_playwright()
            page = self._playwright_context.new_page()
            page.goto(url, timeout=self.playwright_timeout)
            if wait_selector:
                try:
                    page.wait_for_selector(wait_selector, timeout=self.playwright_timeout)
                except PlaywrightTimeoutError:
                    pass
            html = page.content()
            page.close()
            return html
        except Exception as e:
            print(f"_fetch_html_with_playwright error: {e}")
            return ''

    # ---- getTimeToken ----
    def getTimeToken(self):
        try:
            res = requests.get(self.home_url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(res.content, 'html.parser')
            t_input = soup.find('input', attrs={'name': 't'})
            if t_input and t_input.get('value'):
                return re.sub(r'==$', '%3D%3D', t_input.get('value'))
        except Exception:
            pass

        html = self._fetch_html_with_playwright(self.home_url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            t_input = soup.find('input', attrs={'name': 't'})
            if t_input and t_input.get('value'):
                return re.sub(r'==$', '%3D%3D', t_input.get('value'))
        return ''

    # ---- homeContent ----
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
                # filters 可照原本完整保留
            }
        }
        return result

    # ---- homeVideoContent ----
    def homeVideoContent(self):
        d = []
        try:
            html = self._fetch_html_with_playwright(self.home_url, wait_selector="div.module-item a.v-item")
            if not html:
                return {"list": d, "parse": 0, "jx": 0}
            root = etree.HTML(html)
            items = root.xpath('//div[contains(@class,"module-item")]//a[contains(@class,"v-item")]')
            for i in items:
                hrefs = i.xpath('./@href')
                vod_id = hrefs[0] if hrefs else ''
                title_list = i.xpath('.//div[contains(@class,"v-item-title")]/text()')
                pic = i.xpath('.//img/@data-original') or i.xpath('.//img/@src') or ['']
                vod_name = title_list[0].strip() if title_list else ''
                vod_pic = pic[0].strip() if pic and pic[0] else ''
                if vod_pic and not vod_pic.startswith('http'):
                    vod_pic = self.image_domain.rstrip('/') + '/' + vod_pic.lstrip('/')
                remarks = ''.join(i.xpath('.//div[contains(@class,"v-item-bottom")]//span/text()')).strip()
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
            print("homeVideoContent error:", e)
            return {"list": [], "parse": 0, "jx": 0}

    # ---- categoryContent ----
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

    # ---- detailContent ----
    def detailContent(self, did):
        ids = did[0] if isinstance(did, (list, tuple)) and len(did) > 0 else did
        if not ids:
            return {'list': [], 'parse': 0, 'jx': 0}
        url = self.home_url + ids if ids.startswith('/') else self.home_url + '/' + ids
        try:
            html = self._fetch_html_with_playwright(url, wait_selector='div.episode-list')
            if not html:
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
                pairs = [_n + '$' + _u for _n, _u in zip(name_list, url_list)]
                if pairs:
                    vod_play_url_list.append('#'.join(pairs))
            vod_play_url = '$$$'.join(vod_play_url_list)
            vod_name = (root.xpath('//h1/text()') or [''])[0].strip()
            vod_content = ''.join(root.xpath('//div[contains(@class,"video-desc")]//text()')).strip() or ''
            vod_actor = ''.join(root.xpath('//div[contains(@class,"actor")]//text()')).strip() or ''
            vod_director = ''.join(root.xpath('//div[contains(@class,"director")]//text()')).strip() or ''
            return {"list": [{
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
            }], 'parse': 0, 'jx': 0}
        except Exception as e:
            print(f"detailContent error: {e}")
            return {'list': [], 'msg': str(e)}

    # ---- searchContent ----
    def searchContent(self, key, quick, page='1'):
        token = self.getTimeToken()
        url = f'{self.home_url}/search?k={key}'
        if token:
            url += f'&t={token}'
        d = []
        try:
            res = requests.get(url, headers=self.headers, timeout=15)
            html = res.text if res.status_code == 200 else ''
            root = etree.HTML(html) if html else None
            data_list = root.xpath('//a[contains(@class,"search-result-item")]') if root else []
            if not data_list:
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
            return {'list': d, 'parse': 0, 'jx': 0}
        except Exception as e:
            print(f"searchContent error: {e}")
            return {'list': [], 'parse': 0, 'jx': 0}

    # ---- playerContent ----
    def playerContent(self, flag, pid, vipFlags):
        url = self.home_url + pid if pid.startswith('/') else (pid if pid.startswith('http') else self.home_url + '/' + pid)
        try:
            res = requests.get(url, headers=self.headers, timeout=15)
            text = res.text or ''
            play_url_list = re.findall(r'src[:=]\s*"(https?://[^"]+)"', text)
            if not play_url_list:
                html = self._fetch_html_with_playwright(url, wait_selector='video, iframe, source')
                if html:
                    play_url_list = re.findall(r'src[:=]\s*"(https?://[^"]+)"', html)
                if not play_url_list and html:
                    root = etree.HTML(html)
                    play_url_list = (root.xpath('//video/source/@src') or root.xpath('//video/@src') or root.xpath('//iframe/@src') or [])
            if play_url_list:
                return {'url': play_url_list[0], 'parse': 0, 'jx': 0, 'header': {"User-Agent": "okhttp/5.0.0"}}
            return {'url': url, 'parse': 1, 'jx': 0}
        except Exception as e:
            print(f"playerContent error: {e}")
            return {'url': self.default_play_url, 'parse': 0, 'jx': 0}

    def localProxy(self, params):
        return None

    def destroy(self):
        self._close_playwright()
        return '正在Destroy'


if __name__ == '__main__':
    pass
