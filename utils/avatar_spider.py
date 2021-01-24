import requests
from fake_useragent import UserAgent
from lxml import etree
from bbs import settings

home_url = "https://www.woyaogexing.com/touxiang/katong/new/"
resp = requests.get(home_url, headers={"User-Agent": UserAgent().chrome})
if resp.status_code == 200:
    doc = etree.HTML(resp.text)
    urls = doc.xpath('//a[@class="img"]/img/@src')
    for i, url in enumerate(urls):
        print(url)
        img_resp = requests.get("http:" + url, headers={"User-Agent": UserAgent().chrome})
        if img_resp.status_code == 200:
            filename = 'avatar%s%s' % (i, url[url.rfind("."):])
            with open("%s\\avatars\\%s" % (settings.BASE_DIR, filename), "wb") as file:
                file.write(img_resp.content)
