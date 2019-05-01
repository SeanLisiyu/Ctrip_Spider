# coding=utf-8
import os
import requests as req
import http.client as http_client
import http.cookiejar as cookielib
import re
import time
import hmac
import hashlib
import base64
from PIL import Image
import matplotlib.pyplot as plt
import json
#import brotli
import execjs

# zhihui_url = "https://www.zhihu.com/"
# session = req.session()
# session.cookies = cookielib.LWPCookieJar(filename="cookie.txt",)
# agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
# accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
"""
:authority: www.zhihu.com
:method: GET
:path: /signup?next=%2F
:scheme: https
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
cache-control: max-age=0
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36
"""

# headers = {
#     ":authority": "www.zhihu.com",
#     ":method": "GET",
#     ":path" : "/signup?next=%2F",
#     ":scheme": "https",
#     "accept": accept,
#     "accept-encoding": "gzip, deflate,br",
#     "cache-control": "max-age=0",
#     "upgrade-insecure-requests": "1",
#     "user-agent": agent
# }
# header = {
#     "HOST": "www.zhihu.com",
#     "Referer": "www.zhihu.com",
#     "user-agent": agent
# }
# http_client._is_legal_header_name = re.compile(rb'\A[^\s][^\r\n]*\Z').match
# response = session.get(zhihui_url,headers=headers)
# str=response.content
# str = brotli.decompress(str)
# session.cookies.save()
# print(str.decode('utf-8'))
# print("你好")

"""
captcha: "{"img_size":[200,43.99739456176758],"input_points":[[95.4296875,27.1171875],[15.4296875,18.1171875]]}"
clientId: "c3cef7c66a1843f8b3a9e6a1e3160e20"
clientId: "c3cef7c66a1843f8b3a9e6a1e3160e20"
grantType: "password"
lang: "cn"
password: "lsy13485340785,"
refSource: "homepage"
signature: "09c4a88333148a7fe743dc0f5ad94b7f06ce3601"
source: "com.zhihu.web"
timestamp: 1554132846631
username: "+8618221669254"
utmSource: ""
"""
"""
captcha: "g9tp"
clientId: "c3cef7c66a1843f8b3a9e6a1e3160e20"
grantType: "password"
lang: "en"
password: "12345678"
refSource: "homepage"
signature: "980a232011ffee005dd6dfb478dffed717295ddb"
source: "com.zhihu.web"
timestamp: 1554730012801
username: "+8618221669254"
utmSource: ""
"""
"""
:authority: www.zhihu.com
:method: POST
:path: /api/v3/oauth/sign_in
:scheme: https
accept: */*
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
content-length: 396
content-type: application/x-www-form-urlencoded
cookie: _xsrf=8jb25OsouQzb6wiUcoHKWtvw5FZwULlc; tgw_l7_route=060f637cd101836814f6c53316f73463; _zap=0cd3b10f-eacc-424b-b35f-ecb8df3c7254; d_c0="AOClc4CiQA-PTnLYQbCWcweswMK1ZIB57gw=|1554815603"; capsion_ticket="2|1:0|10:1554815604|14:capsion_ticket|44:OWFlZDJhNTNiNzIxNDVmOGE4ZWIwZmM0NmFhNDkyMmY=|3b18e7404362572337f2320edef8544cddb941ac144f8268b85d7a29a281a216"
origin: https://www.zhihu.com
referer: https://www.zhihu.com/signin?next=%2F
user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36
x-ab-param: se_page_limit_20=1;top_bill=0;tp_sft=a;ug_follow_answerer_0=0;li_gbdt=2;se_click_del=0;se_topicseed=1;top_native_answer=1;top_ntr=1;top_rank=0;li_filter_ttl=2;pf_feed=1;se_webrs=1;se_zu_recommend=0;li_lt_tp_score=1;se_expired_ob=0;se_preset_tech=0;se_topic=0;top_user_cluster=0;ug_newtag=0;tp_qa_metacard_top=top;li_ts_sample=old;pf_noti_entry_num=0;se_likebutton=0;top_ebook=0;top_reason=1;top_recall_exp_v2=1;top_test_4_liguangyi=1;zr_answer_rec=close;se_consulting_price=n;top_ydyq=X;se_domain_onebox=0;se_new_market_search=on;pf_foltopic_usernum=50;se_wannasearch=0;se_threshold=4;top_hotcommerce=1;top_zh_tailuser=1;zr_ans_rec=gbrank;zr_rel_search=base;se_ltr_0318=0;se_rr=0;top_tabvideo=1;zr_art_rec=base;li_se_highlight=1;qa_answerlist_ad=0;se_consulting_switch=off;se_entity=on;top_source=0;se_ios_spb309=0;se_site_onebox=0;tp_discussion_feed_type_android=2;zr_km_material_buy=2;tp_sticky_android=0;ug_follow_answerer=0;top_root=0;top_universalebook=1;zr_feed_cf=1;pf_fuceng=1;se_bertv=0;se_km_ad_locate=1;se_spb309=0;top_billupdate1=2;qa_video_answer_list=0;se_ad_index=10;se_ios_spb309bugfix=0;top_video_rerank=-1;qa_web_answerlist_ad=1;se_major_onebox=major;top_vipoffice=1;li_album_liutongab=0;ls_fmp4=0;se_auto_syn=0;top_vipconsume=1;tp_header_style=1;ug_follow_topic_1=2;li_es_new=new;li_se_ebook_chapter=1;qa_test=0;se_config=1;se_websearch=3;se_billboardsearch=0;tp_m_intro_re_topic=1;tp_qa_metacard=1;gw_guide=0;se_roundtable=0;se_se_index=0;top_new_user_rec=0;tsp_lastread=0;li_se_intervene=1;se_minor_onebox=d;se_zu_onebox=0;se_decoupling=0;se_sensitive=0;top_quality=0;top_wonderful=1;ug_zero_follow_0=0;pf_creator_card=1;se_lottery=0;se_result_time=0;se_webtimebox=0;top_recall_deep_user=1;top_sess_diversity=-1;pf_newguide_vertical=0;se_terminate=0;soc_bigone=0;top_recall_exp_v1=1;se_backsearch=0;top_nucc=0;zr_video_rec=zr_video_rec:base;se_click_limit=0;se_search_feed=N;soc_special=0;ug_zero_follow=0;zr_article_rec_rank=truncate;se_webmajorob=0;top_new_feed=5;top_v_album=1;zr_search_material=0;top_gr_ab=0;tp_sft_v2= a;ug_fw_answ_aut_1=0;se_payconsult= 0;se_p_slideshow=0
x-requested-with: fetch
x-xsrftoken: 8jb25OsouQzb6wiUcoHKWtvw5FZwULlc
x-zse-83: 3_1.1
"""


class LoginZhiHu:
    url = "https://www.zhihu.com/"
    captcha_url = "https://www.zhihu.com/api/v3/oauth/captcha?lang=cn"
    login_url = "https://www.zhihu.com/api/v3/oauth/sign_in"
    agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
    accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
    x_ab_param = "top_rank=0;li_gbdt=2;top_new_user_rec=0;pf_fuceng=0;se_site_onebox=0;top_ebook=0;top_zh_newuser=1;tp_qa_metacard_top=top;li_filter_ttl=2;pf_creator_card=1;se_se_index=0;se_topicseed=1;se_webmajorob=0;li_es_new=new;qa_web_answerlist_ad=0;ug_follow_topic_1=2;pf_feed=3;top_gr_ab=0;top_source=0;pf_newguide_vertical=1;se_auto_syn=0;zr_search_material=0;li_lt_tp_score=1;se_ios_spb309=0;qa_video_answer_list=0;se_websearch=3;top_quality=0;top_billupdate1=2;top_new_feed=5;tp_m_intro_re_topic=1;se_qanchor=1;se_rr=0;se_ios_spb309bugfix=0;se_km_ad_locate=1;tp_qa_metacard=1;ug_follow_answerer=0;se_terminate=0;top_universalebook=1;top_native_answer=1;zr_feed_cf=1;zr_km_material_buy=2;li_se_ebook_chapter=1;se_spb309=0;zr_ans_rec=gbrank;top_recall_exp_v2=1;top_zh_tailuser=1;soc_bigone=0;zr_article_rec_rank=truncate;se_decoupling=0;se_page_limit_20=1;tp_sticky_android=0;li_se_intervene=1;top_ntr=1;top_bill=0;top_test_4_liguangyi=1;tp_sft=a;ug_zero_follow_0=0;qa_test=0;se_click_del=0;top_sess_diversity=-1;se_ltr_0318=0;se_webtimebox=0;soc_special=0;top_video_rerank=-1;top_wonderful=1;se_minor_onebox=d;se_preset_tech=0;top_tabvideo=1;ug_newtag=0;se_domain_onebox=0;se_lottery=0;se_threshold=4;top_root=0;se_expired_ob=0;se_likebutton=0;tp_discussion_feed_type_android=2;zr_art_rec=base;zr_rel_search=base;zr_video_rec=zr_video_rec:base;top_hotcommerce=1;top_vipoffice=1;top_recall_deep_user=1;ug_zero_follow=0;se_zu_onebox=0;top_reason=1;se_consulting_price=n;se_topic=0;se_wannasearch=0;zr_answer_rec=close;li_album_liutongab=0;pf_foltopic_usernum=0;se_zu_recommend=0;top_v_album=1;li_se_highlight=1;se_entity=on;se_config=1;se_consulting_switch=off;se_p_slideshow=0;se_roundtable=0;top_recall_exp_v1=1;top_user_cluster=0;gw_guide=0;ls_fmp4=0;top_vipconsume=1;li_ts_sample=old;se_ad_index=10;se_new_market_search=on;top_nucc=0;top_ydyq=X;tp_sft_v2= a;pf_noti_entry_num=0;se_billboardsearch=0;se_major_onebox=major;tp_header_style=1;tsp_lastread=0;qa_answerlist_ad=0;se_backsearch=0;se_sensitive=0;se_webrs=1;top_re_sametag=0;se_bertv=0;se_search_feed=N"
    session = req.session()
    http_client._is_legal_header_name = re.compile(rb'\A[^\s][^\r\n]*\Z').match
    login_data = {
        "clientId": "c3cef7c66a1843f8b3a9e6a1e3160e20",
        "grantType": "password",
        "source": "com.zhihu.web"
    }
    login_header = {
        "content-type": "application/x-www-form-urlencoded",
        "x-zse-83": "3_1.1"
    }
    cookie_file_name=""

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.timestamp = str(int(time.time() * 1000))
        print("模拟登陆知乎")

    def make_open_headers(self):
        open_headers =  {
             ":authority": "www.zhihu.com",
             ":method": "GET",
             ":path" : "/signup?next=%2F",
             ":scheme": "https",
             "accept": self.accept,
             "accept-encoding": "gzip, deflate,br",
             "cache-control": "max-age=0",
             "upgrade-insecure-requests": "1",
             "user-agent": self.agent
        }
        return open_headers

    def make_captcha_headers(self):
        captcha_headers = {
            ":authority" : "www.zhihu.com",
            ":method" : "GET",
            # ":path": "/ api / v3 / oauth / captcha?lang = en",
            ":scheme" : "https",
            "accept" : "* / *",
            "accept - encoding" : "gzip, deflate, br",
            "accept - language": "zh - CN, zh;q = 0.9",
            "if -none - match" : "7eb4ebdc523b46e04c7fa978993f57f559d7ed8b",
            "referer: https": "https:// www.zhihu.com / signup?next = % 2f",
            "user-agent": self.agent,
            # "x-ab-param" : self.x_ab_param,
            "x-requested-with": "fetch"
        }
        return captcha_headers

    def get_xsrftoken(self,cookie_filename):
        cookie_file = open(cookie_filename,mode="r",encoding="utf-8")
        set_cookie = cookie_file.read()
        xrftoken = re.findall("_xsrf=(.*?);",set_cookie)[0]
        return  xrftoken

    def make_login_headers(self,cookie_filename):
        xsrftoken = self.get_xsrftoken(cookie_filename)
        self.login_header.update(
            {
                "x-xsrftoken": xsrftoken,
                "user-agent": self.agent
            }
        )

    def start_open_index(self):
        headers = self.make_open_headers()
        response = self.session.get(self.url,headers=headers)
        return response

    def make_filepath(self,filename):
        current_dir = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(current_dir, 'ZhiHu_') + filename
        return file_path

    def get_start_cookies(self):
        filename = self.make_filepath("cookie.txt")
        print("store ZhiHu cookie in " + filename)
        self.session.cookies = cookielib.LWPCookieJar(filename=filename)
        self.start_open_index()
        self.session.cookies.save()
        self.cookie_file_name = filename
        return filename

    def get_signature(self,timestamp):
        ha = hmac.new(b'd1b964811afb40118a12068ff74a12f4', digestmod=hashlib.sha1)
        grant_type = self.login_data['grantType']
        client_id = self.login_data['clientId']
        source = self.login_data['source']
        ha.update(bytes((grant_type + client_id + source + timestamp), 'utf-8'))
        return ha.hexdigest()

    def get_captcha(self):
        captcha_headers_1 = self.make_captcha_headers()
        response_1 = self.session.get(self.captcha_url, headers=captcha_headers_1)
        captcha_show = re.search("true", response_1.text)
        lang = re.findall("lang=(.*?)", self.captcha_url, re.S)[0].strip()
        if captcha_show:
            print("需要验证码")
            put_response = self.session.put(self.captcha_url,headers=captcha_headers_1)
            img_base64 = re.findall('"img_base64":"(.*?)"', put_response.text, re.S)[0].replace("\\n","")
            captcha_filename = "./captcha.jpg"
            with open(captcha_filename,'wb') as f:
                f.write(base64.b64decode(img_base64))
                img = Image.open('captcha.jpg')
            if lang == "en":
                img.show()
                capt_para = input("请输入图中验证码")
            else:
                plt.imshow(img)
                points = plt.ginput(7)  # Settings | Tools | Python Scientific | Show Plots in Toolwindow，去掉对勾
                n = input("输入倒立字个数 ")
                capt_para = json.dumps({'img_size': [200, 44],
                                        'input_points': [[i[0]/2, i[1]/2] for i in points[0:int(n)]]})
            # self.session.post(self.captcha_url, data={"input_text": capt_para})
            # print(capt_para)
            return capt_para
        else:
            print("不需要验证码")
            return ""

    def make_form_data(self,captcha):
        timestamp = str(int(time.time() * 1000))
        self.login_data.update(
            {
                'captcha': captcha,
                'lang': re.findall("lang=(.*?)", self.captcha_url, re.S)[0].strip(),
                'password': self.password,
                'refSource':"homepage",
                'signature': self.get_signature(timestamp),
                'timestamp': timestamp,
                'username': self.username,
                'utmSource': ""
            }
        )
        text = "client_id=c3cef7c66a1843f8b3a9e6a1e3160e20&grant_type=password&timestamp={0}&" \
               "source=com.zhihu.web&signature={1}&username=%2B86{2}&password={3}&" \
               "captcha={4}&lang=cn&ref_source=homepage&utm_source=".format(self.login_data['timestamp'], self.login_data['signature'], self.username, self.password, self.login_data['captcha'])
        # e = "client_id=c3cef7c66a1843f8b3a9e6a1e3160e20&grant_type=password&timestamp=1554734034444&source=com.zhihu.web&signature=c3b202f19b4d06c73eb35a7b735aeabc4197af2f&username=%2B8618221669254&password=12345678&captcha=pusk&lang=en&ref_source=homepage&utm_source="
        with open('./encrypt.js',encoding='utf-8') as f:
            js = execjs.compile(f.read())
            encrypt_data = js.call('Q', text)
        return encrypt_data

    def verify_captcha(self, captcah):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        }
        response = self.session.post(self.captcha_url, headers=headers,data={"input_text": captcah})
        if "true" in response.text:
            return True
        else:
            return False

    def login(self,login_headers,formadata):
        # self.start_open_index()
        # cookie_filename = self.get_start_cookies()
        # login_headers = self.make_login_headers(cookie_filename)
        # captcha = self.get_captcha()
        # if self.verify_captcha(captcha):
        response = self.session.post(self.login_url, headers=login_headers, data=formadata)
        return response

    def ZhiHu(self):

        cookie_filename = self.get_start_cookies()
        self.make_login_headers(cookie_filename)
        captcha = self.get_captcha()

        if captcha:
            while not self.verify_captcha(captcha):
                captcha = self.get_captcha()

        formdata = self.make_form_data(captcha)
        response = self.login(self.login_header, formdata)
        print("login status_code: " + str(response.status_code))
        return response

    def verify_login(self):
        resp = self.session.get('https://www.zhihu.com/', headers=self.login_header)
        if "推荐" in resp.text:
            print("登录成功")
            self.session.cookies.save()
            return True
        else:
            print("登录失败")
            return False

    def read_cookie_login(self):
        try:
            resp = self.session.cookies.load()
            print("加载cookie成功")
        except:
            print("cookie 未加载")
            resp = self.ZhiHu()
        return resp


if __name__ == '__main__':
    
    login = LoginZhiHu("18221669254", "lsy13485340785")
    login.read_cookie_login()
    if login.verify_login():
        resp = login.session.get('https://www.zhihu.com/', headers=login.login_header)
        Indexfile = open("zhihu_index.html",mode="w+",encoding="utf-8")
        Indexfile.write(resp.text)
        Indexfile.close()