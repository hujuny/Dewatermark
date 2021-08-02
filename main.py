# @author yhj
import json
import re
import  webbrowser
import requests
from selenium import webdriver


def get_url(content):
    if len(re.findall('[a-z]+://[\S]+', content, re.I | re.M)) > 0:
        return re.findall('[a-z]+://[\S]+', content, re.I | re.M)[0]
    return None


def get_cookie(url, header):
    # session = requests.Session()
    # req = session.get(url, headers={
    #     'Host': 'www.kuaishou.com',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    #     'Accept-Language': 'zh-CN,zh;q=0.9',
    #     'Accept-Encoding': 'gzip, deflate, br',
    #     'Connection': 'keep-alive'
    # })

    driver = webdriver.PhantomJS()
    driver.get(url)
    # 获取cookie列表
    cookie_list = driver.get_cookies()
    # 格式化打印cookie
    for cookie in cookie_list:
        print(cookie)
    a = ''

    # for i in range(len(session.cookies.keys())):
    #     if i == len(session.cookies.keys()) - 1:
    #         a = a + session.cookies.keys()[i] + '=' + session.cookies.values()[i]
    #     else:
    #         a = a + session.cookies.keys()[i] + '=' + session.cookies.values()[i] + ';'

    return a


def get_redirect_url(url, header):
    # 请求网页
    response = requests.get(url, headers=header)
    print(response.cookies)
    print(response.url)
    return response.url


if __name__ == '__main__':
    douyinUrl = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo'
    kuaishouUrl = 'https://www.kuaishou.com/graphql'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
    inputContent = input('请输入视频链接：')
    # inputContent = '大家评个理，我二狗错了没？       https://v.kuaishou.com/dWEuk4 复制此消息，打开【快手】直接观看！'
    if inputContent.strip() is not None:
        if get_url(inputContent) is not None:
            realUrl = get_redirect_url(get_url(inputContent), headers)
            startUrl = realUrl[0:realUrl.index('?')]
            itemId = startUrl[startUrl.rindex('/') + 1:len(startUrl)]
            douyinParams = {
                'item_ids': itemId
            }
            if realUrl.__contains__('www.douyin.com'):
                douyinResponse = requests.get(url=douyinUrl, params=douyinParams, headers=headers)
                body = douyinResponse.text
                print(douyinResponse.url)
                data = json.loads(body)
                print(data['item_list'][0]['desc'])
                videoUrl = data['item_list'][0]['video']['play_addr']['url_list'][0]
                realVideoUrl = f'{videoUrl}'.replace('playwm', 'play')
                print(realVideoUrl)
                webbrowser.open(realVideoUrl)
            elif realUrl.__contains__('www.kuaishou.com'):
                cookie = get_cookie(get_url(realUrl), headers)
                header = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
                    'Cookie': cookie
                }
                kuaishouData = {
                    'operationName': 'visionVideoDetail',
                    'query': 'query visionVideoDetail($photoId: String, $type: String, $page: String, $webPageArea: String) {\n  visionVideoDetail(photoId: $photoId, type: $type, page: $page, webPageArea: $webPageArea) {\n    status\n    type\n    author {\n      id\n      name\n      following\n      headerUrl\n      __typename\n    }\n    photo {\n      id\n      duration\n      caption\n      likeCount\n      realLikeCount\n      coverUrl\n      photoUrl\n      liked\n      timestamp\n      expTag\n      llsid\n      viewCount\n      videoRatio\n      stereoType\n      croppedPhotoUrl\n      manifest {\n        mediaType\n        businessType\n        version\n        adaptationSet {\n          id\n          duration\n          representation {\n            id\n            defaultSelect\n            backupUrl\n            codecs\n            url\n            height\n            width\n            avgBitrate\n            maxBitrate\n            m3u8Slice\n            qualityType\n            qualityLabel\n            frameRate\n            featureP2sp\n            hidden\n            disableAdaptive\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    tags {\n      type\n      name\n      __typename\n    }\n    commentLimit {\n      canAddComment\n      __typename\n    }\n    llsid\n    danmakuSwitch\n    __typename\n  }\n}\n',
                    'variables': {
                        'page': 'detail',
                        'photoId': itemId
                    }
                }
                print(kuaishouData)
                print(header)
                # kuaishouBody = requests.post(url=kuaishouUrl, data=kuaishouData, headers=headers).text
                # print(kuaishouBody)
                # data = json.loads(kuaishouBody)
                # print(data['data']['visionVideoDetail']['photo']['caption'])
                # print(data['data']['visionVideoDetail']['photo']['photoUrl'])
                # realVideoUrl = data['data']['visionVideoDetail']['photo']['photoUrl']
                # webbrowser.open(realVideoUrl)
