#-*-coding:utf8-*-

import re
import string
import sys
import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import requests
import shutil
import time
from lxml import etree
reload(sys) 
sys.setdefaultencoding('utf-8')

#if(len(sys.argv)>=2):
#        user_id = (int)(sys.argv[1])
#else:
#        user_id = (int)5(raw_input(u"please_input_id: "))

origin_user_id = 5316283802
origin_url = 'http://weibo.cn/u/%d?filter=1&page=1'%origin_user_id
cookie = {"Cookie": "ALF=1508125508; _T_WM=269d02f77989652a9a74bb880a8cd25b; WEIBOCN_WM=3349; H5_wentry=H5; backURL=https%3A%2F%2Flogin.sina.com.cn%2Fsso%2Flogin.php%3Furl%3Dhttps%3A%2F%2Fm.weibo.cn%2F%26_rand%3D1505534106.6278%26gateway%3D1%26service%3Dsinawap%26entry%3Dsinawap%26useticket%3D1%26returntype%3DMETA%26sudaref%3D%26_client_version%3D0.6.26; SCF=AhQ62bGyZQ5sI5vnfy48cl0rHI7WhJYaTvFUHWYs4yn6NSOjwiYFjP4lDlKqmw2WJ2qEIS46ND6hvXWfvWsY3lc.; SUB=_2A250uNEqDeRhGeBP6VAZ8y7EyTiIHXVUQv9irDV6PUJbktBeLWinkW0A7V58P4TdzWBEQXEsh3FEaI9_Tw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Who9J5O0N3rS-sCDj7udzFY5JpX5o2p5NHD95QceKzE1he71hzXWs4Dqc_Fi--Ri-zfi-8Fi--fi-z7iK.Xi--Ri-i8iKLFi--ci-27i-z4i--RiKy8i-8Fi--ciK.ci-8si--RiKnEi-8sSKnf; SUHB=0qj0mqWmG489YT; SSOLoginState=1505534330; M_WEIBOCN_PARAMS=luicode%3D20000174%26uicode%3D20000174%26featurecode%3D20000320%26fid%3Dhotword"}
origin_lxml = requests.get(origin_url, cookies = cookie).content
origin_title_search = r'span class="ctt">(.{1,15})<'
origin_title = str(re.findall(origin_title_search, origin_lxml)[0])
os.mkdir(os.getcwd() + r'/%s及其关注用户资料' % origin_title)
origin_user_focus_url = 'https://weibo.cn/%d/follow' % origin_user_id
foucs_list = requests.get(origin_user_focus_url, cookies = cookie).content
foucs_url_search = r'https://weibo.cn/u/(\d*)'
from_origin_user = re.findall(foucs_url_search, foucs_list)
pages_search = r'value="跳页" />&nbsp;1/(\d*)页'
pages = int(re.findall(pages_search, foucs_list)[0])
print pages
for i in range(2, pages+1):
    origin_user_focus_url_ = 'https://weibo.cn/%d/follow?page=%d' % (origin_user_id, i)
    foucs_list_ = requests.get(origin_user_focus_url_, cookies = cookie).content
    foucs_url_search_ = r'https://weibo.cn/u/(\d*)'
    from_origin_user_ = re.findall(foucs_url_search_, foucs_list_)
    from_origin_user.extend(from_origin_user_)
    time.sleep(1)
from_origin_user.append(origin_user_id)
from_origin_user = list(set(from_origin_user))
print len(from_origin_user)


for user_id in from_origin_user:
    user_id = int(user_id)
#cookie = {"Cookie": "ALF=1508125508; _T_WM=269d02f77989652a9a74bb880a8cd25b; WEIBOCN_WM=3349; H5_wentry=H5; backURL=https%3A%2F%2Flogin.sina.com.cn%2Fsso%2Flogin.php%3Furl%3Dhttps%3A%2F%2Fm.weibo.cn%2F%26_rand%3D1505534106.6278%26gateway%3D1%26service%3Dsinawap%26entry%3Dsinawap%26useticket%3D1%26returntype%3DMETA%26sudaref%3D%26_client_version%3D0.6.26; SCF=AhQ62bGyZQ5sI5vnfy48cl0rHI7WhJYaTvFUHWYs4yn6NSOjwiYFjP4lDlKqmw2WJ2qEIS46ND6hvXWfvWsY3lc.; SUB=_2A250uNEqDeRhGeBP6VAZ8y7EyTiIHXVUQv9irDV6PUJbktBeLWinkW0A7V58P4TdzWBEQXEsh3FEaI9_Tw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Who9J5O0N3rS-sCDj7udzFY5JpX5o2p5NHD95QceKzE1he71hzXWs4Dqc_Fi--Ri-zfi-8Fi--fi-z7iK.Xi--Ri-i8iKLFi--ci-27i-z4i--RiKy8i-8Fi--ciK.ci-8si--RiKnEi-8sSKnf; SUHB=0qj0mqWmG489YT; SSOLoginState=1505534330; M_WEIBOCN_PARAMS=luicode%3D20000174%26uicode%3D20000174%26featurecode%3D20000320%26fid%3Dhotword"}
    url = 'http://weibo.cn/u/%d?filter=1&page=1'%user_id
    html = requests.get(url, cookies = cookie).content
    print u'user_id和cookie读入成功'
    selector = etree.HTML(html)
    try:
        pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
    except:
        continue

    url = 'http://weibo.cn/u/%d?filter=1&page=1'%user_id 
    lxml = requests.get(url, cookies = cookie).content
    title_search = r'<title>(.*)</title>'
    title = str(re.findall(title_search, lxml)[0])
    os.mkdir(os.getcwd() + r'/%s及其关注用户资料' % origin_title + r'/%s_file' % title)

    result = "" 
    urllist_set = set()
    word_count = 1
    image_count = 1

    print u'ready'
    print pageNum
    sys.stdout.flush()

    times = 5
    one_step = pageNum/times

    for step in range(times):
        if step < times - 1:
            i = step * one_step + 1
            j =(step + 1) * one_step + 1
        else:
            i = step * one_step + 1
            j =pageNum + 1
        for page in range(i, j):
            #获取lxml页面
            #try:
            url = 'http://weibo.cn/u/%d?filter=1&page=%d'%(user_id,page) 
            lxml = requests.get(url, cookies = cookie).content
                #文字爬取
            try:
                selector = etree.HTML(lxml)
                content = selector.xpath('//span[@class="ctt"]')
            except:
                continue
            for each in content:
                text = each.xpath('string(.)')
                if word_count >= 3:
                    text = "%d: "%(word_count - 2) +text+"\n"
                else :
                    text = text+"\n\n"
                result = result + text
                word_count += 1
            print page,'word ok'
            sys.stdout.flush()
            if page == 1:
                head_pic_1 = r'http://tva(.{0,10}).sinaimg.cn/crop.'
                head_pic_2 = r'.sinaimg.cn/crop.(.{0,90}).jpg'
                try:
                    head_pic_link = 'http://tva' + str(re.findall(head_pic_1, lxml)[0]) + '.sinaimg.cn/crop.'
                    head_pic_link = head_pic_link + str(re.findall(head_pic_2, lxml)[0]) + '.jpg'
                except:
                    continue
                #print head_pic_link
#           except:
 #               print page, 'error'
        #print page
            sys.stdout.flush()
        #time.sleep(1)
        print u'正在进行第', step + 1, u'次停顿，防止访问次数过多'
        time.sleep(1)

    try:
        fo = open(os.getcwd() + r'/%s及其关注用户资料' % origin_title + r'/%s_file' % title + '/%d' % user_id, "wb")
        fo.write(result)
        word_path=os.getcwd()+ r'/%s及其关注用户资料' % origin_title + r'/%s_file' % title + '/%d' % user_id
        print u'文字微博爬取完毕'
    except:
        print u'存放数据地址有误'
    print u'原创微博爬取完毕，共%d条，保存路径%s'%(word_count - 3,word_path)

    image_path = os.getcwd() + r'/%s及其关注用户资料' % origin_title + r'/%s_file' % title + '/%d.jpg' % user_id
    r = requests.get(head_pic_link)
    if r.status_code == 200:
        f_headpic = open(image_path, 'w')
        f_headpic.write(r.content)
        f_headpic.close()
        print u'用户头像下载成功'
    else:
        print u"该图片下载失败:%s"%head_pic_link