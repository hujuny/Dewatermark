# @author yhj
import json
import re
import webbrowser
import requests


def get_url(content):
    if len(re.findall('[a-z]+://[\S]+', content, re.I | re.M)) > 0:
        return re.findall('[a-z]+://[\S]+', content, re.I | re.M)[0]
    return None


def get_redirect_url(url, header):
    # url:重定向的url
    response = requests.get(url, headers=header)
    return response.url


def douyin_batch():
    response = requests.get(url=douyinUrl, params=douyinParams, headers=headers)
    return response.text


def write_link():
    for content in data['aweme_list']:
        with open('douyin.md', 'a', encoding='utf-8') as f:
            if content.get('video') is None:
                if content.get('image_infos') is not None:
                    if len(content['image_infos'][0]['label_large']['url_list']) > 0:
                        f.write(
                            '[' + content['desc'] + ']' + '(' + content['image_infos'][0]['label_large']['url_list'][
                                0] + ')' + '  <br />')
            elif len(content['video']['play_addr']['url_list']) > 0:
                f.write(
                    '[' + content['desc'] + ']' + '(' + content['video']['play_addr']['url_list'][0] + ')' + '  <br />')


if __name__ == '__main__':
    douyinUrl = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.107 Safari/537.36'}
    inputContent = input('请输入视频链接：')
    if inputContent.strip() is not None:
        if get_url(inputContent) is not None:
            realUrl = get_redirect_url(get_url(inputContent), headers)
            # realUrl：重定向得到的url
            startUrl = realUrl[0:realUrl.index('?')]
            id = startUrl[startUrl.rindex('/') + 1:len(startUrl)]
            douyinParams = {
                'item_ids': id
            }
            if realUrl.__contains__('www.douyin.com/video'):

                douyinResponse = requests.get(url=douyinUrl, params=douyinParams, headers=headers)
                body = douyinResponse.text
                print(douyinResponse.url)
                data = json.loads(body)
                print(data['item_list'][0]['desc'])
                # 视频文案
                videoTitle = data['item_list'][0]['desc']
                # 视频带水印url
                videoUrl = data['item_list'][0]['video']['play_addr']['url_list'][0]
                realVideoUrl = f'{videoUrl}'.replace('playwm', 'play')
                print(realVideoUrl)
                webbrowser.open(realVideoUrl)
            elif realUrl.__contains__('www.douyin.com/user'):
                # headers = {
                #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                #                   'Chrome/92.0.4515.107 Safari/537.36'}
                #
                # realUrl = get_redirect_url(get_url(inputContent), headers)
                # startUrl = realUrl[0:realUrl.index('?')]
                # id = startUrl[startUrl.rindex('/') + 1:len(startUrl)]
                print(id)
                douyinUrl = 'https://www.iesdouyin.com/web/api/v2/aweme/post/'
                douyinParams = {
                    'sec_uid': id,
                    'count': 24,
                    'max_cursor': 0,
                    # 'aid': '1128',
                    # '_signature': 'R8qxlhATHPXt5fEW4KBhFkfKsY'
                }
                body = douyin_batch()
                data = json.loads(body)

                if len(data['aweme_list']) == 0:
                    print('无视频')
                    exit()
                write_link()


                while data['has_more']:
                    input("获取下一页[回车]")
                    douyinParams = {
                        'sec_uid': id,
                        'count': 24,
                        'max_cursor': data['max_cursor'],
                    }
                    body = douyin_batch()
                    data = json.loads(body)
                    write_link()
                print('所有视频已经获取完毕')
