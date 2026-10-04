# </node>
# <node id="844644521" visible="true" version="10" changeset="154594614" timestamp="2024-07-30T08:58:25Z" user="Zenfiric" uid="182327" lat="43.1253360" lon="131.9062099">
#  <tag k="bus" v="yes"/>
#  <tag k="name" v="Владивостокский Государственный Университет"/>
#  <tag k="public_transport" v="stop_position"/>
# </node>

# </node>
# <node id="844644528" visible="true" version="12" changeset="154594614" timestamp="2024-07-30T08:58:25Z" user="Zenfiric" uid="182327" lat="43.1220870" lon="131.9070373">
#  <tag k="bus" v="yes"/>
#  <tag k="name" v="Некрасовская, 50"/>
#  <tag k="public_transport" v="stop_position"/>
# </node>

from bs4 import BeautifulSoup
from math import radians, sin, cos, asin, sqrt
from itertools import combinations
import urllib.request


def count_stop_position():
    xml = open('map.xml', 'r', encoding='utf8').read()
    soup = BeautifulSoup(xml, 'xml')

    cnt = 0
    for node in soup.find_all('node'):
        for tag in node('tag'):
            if tag['k'] == 'public_transport' and tag['v'] == 'stop_position':
                cnt += 1

    print('Количество остановок:', cnt)


def count_sushi_bar():
    xml = open('map.xml', 'r', encoding='utf8').read()
    soup = BeautifulSoup(xml, 'xml')

    cnt = 0
    for node in soup.find_all('node'):
        for tag in node.find_all('tag'):
            v = tag.get('v', '').lower()
            if (tag.get('k') == 'name' and 'суши' in v) or \
                    (tag.get('k') == 'cuisine' and 'sushi' in v):
                cnt += 1
    print('Количество суши-баров:', cnt)


def distance(lat1, lon1, lat2, lon2):
    R = 6371000  # радиус Земли, м
    p1, p2 = radians(lat1), radians(lat2)
    dphi = p2 - p1
    dl = radians(lon2 - lon1)
    a = sin(dphi / 2) ** 2 + cos(p1) * cos(p2) * sin(dl / 2) ** 2
    return 2 * R * asin(sqrt(a))


def distance_from_bus_stops():
    xml = open('map.xml', 'r', encoding='utf8').read()
    soup = BeautifulSoup(xml, 'xml')

    # остановки: (номер, имя, lat, lon, id)
    stops = []
    for node in soup.find_all('node'):
        name = None
        is_stop = False
        for tag in node.find_all('tag'):
            if tag['k'] == 'name':
                name = tag['v']
            if tag['k'] == 'public_transport' and tag['v'] == 'stop_position':
                is_stop = True
        if is_stop:
            stops.append((len(stops) + 1, name or '(без названия)',
                          float(node['lat']), float(node['lon']), node['id']))

    # 1. список остановок

    # 2. нужная пара
    def find(part):
        part = part.lower()
        for s in stops:
            if part in s[1].lower():
                return s

    a = find('Владивостокский Государственный Университет')
    b = find('Некрасовская, 50')
    print('\nВГУЭС – Некрасовская, 50: %.0f м' % distance(a[2], a[3], b[2], b[3]))

    # 3. все пары, отсортированные по расстоянию
    pairs = []
    for s1, s2 in combinations(stops, 2):
        pairs.append((distance(s1[2], s1[3], s2[2], s2[3]), s1, s2))
    pairs.sort(key=lambda p: p[0])

    print('\nВСЕ ПАРЫ ОСТАНОВОК (по возрастанию расстояния):')
    for d, s1, s2 in pairs:
        print('%4.0f м   [%d] %s  –  [%d] %s' % (d, s1[0], s1[1], s2[0], s2[1]))

    print('\nМинимум: %.0f м  ([%d] %s – [%d] %s)' %
          (pairs[0][0], pairs[0][1][0], pairs[0][1][1], pairs[0][2][0], pairs[0][2][1]))
    print('Максимум: %.0f м  ([%d] %s – [%d] %s)' %
          (pairs[-1][0], pairs[-1][1][0], pairs[-1][1][1], pairs[-1][2][0], pairs[-1][2][1]))


def vvsu_dvfu():
    def center(kind, osm_id):
        """Центр объекта OSM (way или relation) как среднее координат его узлов"""
        url = f'https://www.openstreetmap.org/api/0.6/{kind}/{osm_id}/full'
        req = urllib.request.Request(url, headers={'User-Agent': 'student-lab3'})
        data = urllib.request.urlopen(req).read().decode('utf8')
        soup = BeautifulSoup(data, 'xml')

        points = {}  # id узла -> (lat, lon), без повторов
        for node in soup.find_all('node'):
            points[node['id']] = (float(node['lat']), float(node['lon']))

        lat = sum(p[0] for p in points.values()) / len(points)
        lon = sum(p[1] for p in points.values()) / len(points)
        print(f'{kind} {osm_id}: узлов {len(points)}, центр {lat:.6f}, {lon:.6f}')
        return lat, lon

    vgues = (43.125336, 131.9062099)  # остановка ВГУЭС из map.xml
    tgmu = center('way', 168692957)  # ТГМУ
    dvfu = center('relation', 2972043)  # ДВФУ

    print('ВГУЭС – ТГМУ: %.2f км' % (distance(*vgues, *tgmu) / 1000))
    print('ВГУЭС – ДВФУ: %.2f км' % (distance(*vgues, *dvfu) / 1000))


if __name__ == '__main__':
    count_stop_position()
    print(110 * '#')
    count_sushi_bar()
    print(110 * '#')
    distance_from_bus_stops()
    print(110 * '#')
    vvsu_dvfu()
