# encoding:utf-8

import json
import hashlib
import string
import random
import urllib.parse

from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from datetime import timedelta
from django.utils import timezone

from .models import SMS, SMSRecord
from .response_content import ResponseContent


class SMSCaptcha(object):
    __root_url = 'http://qxt.fungo.cn/Recv_center?'
    __cp_name = 'kttwl'
    __cp_password = 'kttwl01'
    __secret = '6D2282295A96834F215F3A7D86525312'

    __time_space = 5
    __captcha = '【酷町堂】您的验证码是{0}，如非本人操作，请忽略本短信。该验证码将在{1}分钟后失效。'
    __password = '【酷町堂】您已注册酷町堂账号，用户名为您的手机号，密码为{0}，请尽快登录修改密码，以防止账号遗失。'


    def send(self, phone, scene):
        captcha = self.__set_captcha(phone, scene)
        content = None
        response = None
        if isinstance(captcha, ResponseContent):
            response = captcha
        else:
            if scene == 4:
                content = self.__password.format(captcha.secret)
            else:
                content = self.__captcha.format(captcha.secret, self.__time_space)
            result = self.__send_sms(
                captcha,
                [phone, ],
                content
            )
            if isinstance(result, ResponseContent):
                response = result
            else:
                response = captcha.secret

        return response

    def __send_sms(self, sms, phone_list, content):
        response = ResponseContent()
        send_url = self.__get_url(phone_list, content)

        try:
            connection = urlopen(send_url)
            connection_json = json.loads(connection.read().decode('utf8'))

            code = connection_json['code']
            smsid = connection_json['smsid']
            CpName = connection_json['CpName']
            SecretSign = connection_json['SecretSign']

            data = code + CpName + smsid + self.__secret
            hash_md5 = hashlib.md5(data.encode('utf-8'))
            compute_sign = hash_md5.hexdigest().lower()

            if smsid.strip() and compute_sign == SecretSign:
                if int(code):
                    response.refresh(code=602, error=code, status='sms')
                else:
                    response = True
            else:
                print("secret_sign error!!!!")
                print("hash_str:" + compute_sign)
                print("secret_sign:" + SecretSign)
                response.refresh(code=602, error=11002)

            record = SMSRecord.objects.create(
                sms=sms,
                code=code,
                cp_name=CpName,
                smsid=smsid,
                secret_sign=SecretSign,
                compute_sign=compute_sign,
                send_time=sms.send_time,
                end_time=sms.end_time,
                scene=sms.scene
            )
            if not record:
                response.refresh(code=201, error=11004)
            else:
                response = record
        except Exception as e:
            response.refresh(code=701, error=e.__str__())

        return response

    def __set_captcha(self, phone, scene):
        result = ResponseContent()

        send_time = timezone.now()
        end_time = send_time + timedelta(minutes=self.__time_space)
        secret = self.__get_code(6)
        try:
            captcha, state = SMS.objects.update_or_create(
                phone=phone,
                defaults={
                    'secret': secret,
                    'phone': phone,
                    'send_time': send_time,
                    'end_time': end_time,
                    'scene': scene,
                    'used': 0
                }
            )
            if captcha:
                result = captcha
            else:
                result.refresh(code=602, error=11003)
        except Exception as e:
            result.refresh(code=701, error=e.__str__())
        return result

    def __get_code(self, count):
        code = []
        for i in range(0, count):
            code.append(str(random.randrange(0, 9)))

        return "".join(code)

    def __get_url(self, phone_list, content):
        des_mobile = ','.join(phone_list)
        content = content.encode('utf8')
        dict = {
            'CpName': self.__cp_name,
            'CpPassword': self.__cp_password,
            'DesMobile': des_mobile,
            'Content': content
        }
        url = self.__root_url + urllib.parse.urlencode(dict)
        return url
