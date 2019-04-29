# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import requests
from bs4 import BeautifulSoup
from xbmcswift2 import Plugin


plugin = Plugin()
session = requests.Session()
session.headers.update(
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 \
            Safari/537.36'})


@plugin.route('/')
def index():
    items = [{
        'label': '直播',
        'path': plugin.url_for('/category/live', page=1)
    }]
    return items


@plugin.route('/category/live')
def live(page):
    url = 'https://api.live.bilibili.com/room/v3/area/getRoomList?platform=web&parent_area_id=1&cate_id=0&area_id=33&sort_type=income&page=1&page_size=60&tag_version=1'
    resp = requests.get(url)
    data = resp.json()
    return [{
        'label': detail['title'],
        'path': plugin.url_for('/category/live', room_id=detail['roomid']),
        'thumbnail': detail['user_cover'],
        'icon': detail['user_cover'],
        'is_playable': True,
    } for detail in data['data']['list']]


@plugin.route('/category/live/<room_id>')
def live_play(room_id):
    resp = session.get('https://live.bilibili.com/{}'.format(room_id))
    soup = BeautifulSoup(resp.content)
    room_info = json.loads(soup.find_all(
        'div', class_='script-requirement').script[0].text[0][31:])
    play_urls = room_info['playUrlRes']['data']['durl']
    plugin.set_resolved_url(play_urls[0]['url'])


if __name__ == "__main__":
    plugin.run()
    plugin.set_view_mode(500)
