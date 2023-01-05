import re
from lxml import etree


def parserRsv(html: str):
    res = []
    h = etree.HTML(html)
    rsv_metainfo = h.xpath('//tbody')
    for i in rsv_metainfo:
        started = False
        rinfo = i.attrib
        seat = i.xpath('.//div[@class="box"]/a/text()')[0]
        startandend = i.xpath('.//span[@class="text-primary"]/text()')
        try:
            aid = i.xpath('.//a[@class="click"]')[0]
            if 'rsvid' in aid.attrib:
                id = aid.attrib['rsvid']
            else:
                id = aid.attrib['onclick']
                id = re.findall('finish\((.*?)\);', id)[0]
                started = True
        except:
            id = ''
        if "已签到" in i.xpath('.//span/text()'):
            signed=True
        else:
            signed=False
        rsv = {
            'id': id,
            'seatname': seat,
            'started': started,
            'start': startandend[0],
            'end': startandend[1],
            'rsv_date': rinfo['date'],
            'signed': signed
        }
        res.append(rsv)
    return res


if __name__ == '__main__':
    with open("./index.html", 'r', encoding='utf-8') as f:
        html = f.read()
    print(parserRsv(html))
