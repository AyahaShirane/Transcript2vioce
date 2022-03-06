# -*- coding: UTF-8 -*-

from http import client
import json, time
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


def get_token(AccessKeyId, AccessKeySecret):
    ali_client = AcsClient(
        AccessKeyId,
        AccessKeySecret,
        "cn-shanghai"
    )

    ali_request = CommonRequest()
    ali_request.set_method('POST')
    ali_request.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
    ali_request.set_version('2019-02-28')
    ali_request.set_action_name('CreateToken')
    ali_response = ali_client.do_action_with_exception(ali_request)
    ali_response_json = json.loads(ali_response)
    return ali_response_json

def TTS_Ali(host, url, http_header, main_body):
    main_body = json.dumps(main_body)
    conn = client.HTTPSConnection(host)
    conn.request(method='POST', url=url, body=main_body, headers=http_header)
    response = conn.getresponse()
    print('Response status and response reason:')
    print(response.status ,response.reason)
    contentType = response.getheader('Content-Type')
    print(contentType)
    log = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'-> response.status:' + str(response.status) + ' | response.reason:' + response.reason + ' | contentType:' + contentType
    voice_result = response.read()
    conn.close()
    if contentType == 'audio/mpeg':
        with open('log.txt', mode='a', encoding='utf-8') as log_file:
            log_file.write('[+]'+log+'\n')
        return voice_result
    else:
        print('The POST request failed: ' + str(voice_result))
        with open('log.txt', mode='a', encoding='utf-8') as log_file:
            log_file.write('[-]ERROR: '+log+'\n')
        return 'ERROR'
