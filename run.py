import re
import pickle
import urllib3
import requests
from lxml import etree

urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
}

result_dict = {}


# Crawling information about computer-related professors at Imperial College London
def imperial_spider():
    response = requests.get('http://www.imperial.ac.uk/computing/people/academic-staff/', headers=headers)
    html_tree = etree.HTML(response.text)
    li_list = html_tree.xpath('//ul[@class="people list"]/li')
    for li in li_list:
        name = li.xpath('.//span[@class="person-name"]/text()')[0]
        if name in result_dict:
            continue
        print(name)
        try:
            url = li.xpath('.//a[@class="name-link"]/@href')[0]
        except:
            url = ''
        mail = li.xpath('.//a[@class="email"]/@href')[0][7:]
        try:
            tel = li.xpath('.//span[@class="tel"]/text()')[0]
        except:
            tel = ''
        address = ''.join(li.xpath('.//div[@class="address-wrapper"]/p//text()'))
        desc = ''.join([i.strip() for i in li.xpath('.//div[@class="dept-wrapper"]/p//text()')])
        result_dict[name] = f'{url}，{mail}，{tel}，{address}，{desc}'


# Crawling information about computer-related professors at Cardiff University
def cardiff_spider():
    response = requests.get('https://www.cardiff.ac.uk/computer-science/people/academic-and-research-staff',
                            headers=headers)
    html_tree = etree.HTML(response.text)
    url_list = html_tree.xpath('//div[@id="new_content_container_119293_119293"]/div//h2/a/@href')
    for url in url_list:
        try:
            r = requests.get(url, headers=headers, verify=False)
        except:
            continue
        html_tree1 = etree.HTML(r.text)
        name = html_tree1.xpath('//h1/text()')[0].replace('\xa0', ' ')
        if name in result_dict:
            continue
        print(name)
        try:
            mail = html_tree1.xpath('//*[@id="content"]/div/div/div[1]/div[1]/div/div[1]/dl/dd[1]/a/text()')[0]
        except:
            mail = ''
        try:
            tel = html_tree1.xpath('//*[@id="content"]/div/div/div[1]/div[1]/div/div[1]/dl/dd[2]/a/text()')[0]
        except:
            tel = ''
        try:
            address = html_tree1.xpath('//*[@class="profile-contact-location"]/text()')[0]
        except:
            address = ''
        desc = ''.join([i.strip() for i in html_tree1.xpath('//*[@id="tab-overview"]//text()')]).replace('\xa0', ' ')
        result_dict[name] = f'{url}，{mail}，{tel}，{address}，{desc}'


# Crawling information about computer-related professors at Newcastle University
def ncl_spider():
    response = requests.get('https://www.ncl.ac.uk/computing/people/academic/',
                            headers=headers)
    html_tree = etree.HTML(response.text)
    url_list = ['https://www.ncl.ac.uk' + i for i in html_tree.xpath('//div[@class="name"]/p/a/@href')]
    for url in url_list:
        try:
            r = requests.get(url, headers=headers, verify=False)
        except:
            continue
        try:
            name = re.findall('displayname" content="(.*?)"', r.text)[0]
        except:
            continue
        if name in result_dict:
            continue
        if name == '':
            continue
        print(name)
        html_tree1 = etree.HTML(r.text)
        try:
            mail = html_tree1.xpath('//li[contains(text(),"Email")]/a/text()')[0]
        except:
            mail = ''
        try:
            tel = html_tree1.xpath('//li[contains(text(),"Telephone")]/text()')[0].replace('Telephone: ', '')
        except:
            tel = ''
        try:
            address = ' '.join(
                [i.strip() for i in html_tree1.xpath('//li[contains(text(),"Address")]/text()')]).replace(
                'Address: ', '')
        except:
            address = ''
        html_string = re.findall('<h2>Background</h2>(.*?)</div>', r.text, re.S)
        if html_string:
            pattern = re.compile(r'<[^>]+>', re.S)
            desc = pattern.sub('', html_string[0]).replace('&nbsp;', ' ')
        else:
            desc = ''
        result_dict[name] = f'{url}，{mail}，{tel}，{address}，{desc}'


if __name__ == '__main__':
    imperial_spider()
    cardiff_spider()
    ncl_spider()
    # Save the acquired information in a dictionary in the form of a pickle file for easy recall
    with open('test.pickle', 'wb') as f:
        pickle.dump(result_dict, f, pickle.HIGHEST_PROTOCOL)

