#coding=utf-8
import requests
import json
import redis
import time
from prettytable import PrettyTable
import os
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl

#
#评论生成动态和评论信息[测试环境]
#批量生成大量的动态和动态的回复
#
class AUTO:
    def __init__(self):
        # 要建立的评论树
        self.feed = '动态-alpha'
        self.comment = ('评论1','评论2')
        self.comment__reply = {
            1: ('回复1' , '回复2' , '回复3' , '回复4' , '回复5' , '回复6' , '回复7' , '回复8' , '回复9' , '回复10' ,
                '回复11', '回复12', '回复13', '回复14', '回复15', '回复16', '回复17', '回复18', '回复19', '回复20' ,
                '回复21', '回复22', '回复23', '回复24', '回复25', '回复26', '回复27', '回复28', '回复29', '回复30' ,
                '回复31', '回复32', '回复33', '回复34', '回复35', '回复36', '回复37', '回复38', '回复39', '回复40' ),
            2: ('回复71', '回复72', '回复73', '回复74', '回复75', '回复76', '回复77', '回复78', '回复79', '回复80'),
            3: ('回复1' , '回复2' , '回复3' , '回复4' , '回复5' , '回复6' , '回复7' , '回复8' , '回复9'),
            4: ('回复1' , '回复2' , '回复3' , '回复4' , '回复5' , '回复6' , '回复7' , '回复8' , '回复9')
        }
        self.generate_res = {}
        #用户信息
        self.cookieString = "4&_device=android&49213e8b-e34a-3349-a7b1-4b3384a3ab4a&6.5.21;4&_token=82030&DBF16AC0B0BA4wEBB4AC07F71F24C58A868EF2F77958F34D;channel=canary;impl=com.ximalaya.ting.android;osversion=26;device_model=RNE-AL00;XUM=7IkUpWq2;XIM=315d46d1c3984;c-oper=%E4%B8%AD%E5%9B%BD%E8%81%94%E9%80%9A;net-mode=WIFI;res=1080%2C2040;NSUP=;AID=DCxrU8F88IA=;manufacturer=HUAWEI;XD=B6gQJbIAiJm9oFLeYWKBrXWQ/1mii14Ak87fg2N9nfRlrfzz1/MMlSmtvqDSSF6eWpR86SbWEoqvhAlxCILAmaMdNGp5+rNE0JI+yh/CyQUe7JThUNE20EUxsZ45cEYQDw6t6nGxSmdUj/b2lD9CLJ+OyNf7pT8J/sZzmPTrBzk=;xm_grade=0;domain=.ximalaya.com;path=/;100709,100892,100691,100569,100703,100870,100627,100322,100889,100891,100791,100799,;x_xmly_resource=xm_source%3Ahomepage%26xm_medium%3Ahomepage;x_xmly_tid=1156487292311783816;x_xmly_ts=1537262853549;"
        # self.cookieString = "domain=.ximalaya.com; path=/; channel=ios-dev; 4&_device=iPhone&DB611248-7E03-43DD-BEA7-5AD888CA60C5&6.5.21; impl=com.gemd.iting; NSUP=42F32E3A%2C41F9AD61%2C1537260915982; XUM=DB611248-7E03-43DD-BEA7-5AD888CA60C5; c-oper=%E6%9C%AA%E7%9F%A5; net-mode=WIFI; res=750%2C1334; 4&_token=80798&9C0FFC707E24340F7CD913FFFAF301F1cDv06A7C79FE835FC7ACD4421A1162F7A6F0882D1E7D6F0A76FFD198302DA003601; idfa=DB611248-7E03-43DD-BEA7-5AD888CA60C5; x_xmly_ts=1537261316771; x_xmly_resource=xm_source%3Afollow; x_xmly_tid=1235475456; device_model=iPhone6s; x-mulehorse-bucketIds=,; XD=2sYogSj9Mb98CeifD1l1W+Th5yaHKdUHibIFyAyNYVe5x4ZQQPUqdgjjxXo2VhCCTZkATDj1vkTE1oVLnSOFKg=="
        self.cookie = {}
        #url
        #域名
        self.local_host = 'http://127.0.0.1:8080'
        self.remote_host = 'http://mobile.test.ximalaya.com/chaos'
        self.host = self.remote_host
        #查询
        self.url_comment_list       = self.host  + '/v3/comment/list?feedId=%s&pageId=%s&pageSize=%s&time=1536846932591'                        #评论列表
        self.url_comment_reply_list = self.host  + '/v3/comment/reply/list?feedId=%s&pageId=%s&pageSize=%s&rootCommentId=%s&time=1536846932591' #评论回复列表
        #创建
        self.url_create_feed        = self.host  + '/v1/feed/create?device=android' #创建动态
        self.url_create_comment     = self.host  + '/v3/feed/comment/create'        #创建评论和评论动态
        #删除
        self.url_delete_comment     = self.host  + '/v1/feed/comment/delete'        #删除动态和动态的回复
        #拉取
        self.url_comment_fetch      = self.host  + '/v1/notice/comment/rec'         #拉取消息

        #返回码
        self.ERROR_CODE_OK = 200 #成功

        #评论id
        self.comment_id_arr         = []
        self.comment_reply_id_arr   = []

        #redis
        self.redis_count_cli   = redis.StrictRedis(host='192.168.3.131',port='19001',password='jredis123456')
        self.redis_info_cli_0  = redis.StrictRedis(host='192.168.1.174',port='6380',password='jredis123456',db=0)
        self.redis_info_cli_1  = redis.StrictRedis(host='192.168.1.174',port='6380',password='jredis123456',db=1)
        #评论数及评论回复数的缓存key
        self.num_comment_query_str       = 'chaos.feed.comments.count_'
        self.num_comment_reply_query_str = 'chaos.comments.reply.count_'
        #获取评论存在缓存中的信息
        self.info_comment_id_list_query_str        = 'updateCommentCache_1_'
        self.info_comment_reply_id_list_query_str  = 'commentReplyCache_1_'
        self.info_comment_obj                      = 'commentObjectCache_%s_1'

    # 产生动态
    def create_feed(self,feed):
        #表单参数
        params = {
            'type' : 1,
            'text' : feed
        }
        try:
            r = requests.post(self.url_create_feed,cookies=self.cookie,data=params)
            if r.status_code == self.ERROR_CODE_OK:
                data = json.loads(r.text)
                feed_id = data['data']['id']
                feed_uid = data['data']['authorInfo']['uid']
                self.generate_res['uid']     = feed_uid
                self.generate_res['feed_id'] = feed_id
                print('创建动态 [ %s ] 成功{feed_id = %s,feed_uid = %s} :)' % (feed,feed_id,feed_uid))
                return True
            else:
                print('创建动态 [ %s ] 失败 :)' % feed)
                return False
        except Exception as e:
            print('创建动态出现异常 :( %s' % e)
            return False

    # 创建评论
    def create_comment(self,comment):
        content = '%s-%s' % (self.feed,comment)
        params = {
            'feedUid': self.generate_res['uid'],
            'feedId': self.generate_res['feed_id'],
            'type': 1,
            'content': content
        }
        try:
            r = requests.post(self.url_create_comment,cookies=self.cookie,data=params)
            if r.status_code == self.ERROR_CODE_OK:
                print('创建动态[ %s ]的评论[ %s ]成功:)' % (self.feed,comment))
                data = json.loads(r.text)
                comment_info = {}
                comment_info['comment_id']  = data['data']['id']
                comment_info['comment_uid'] = data['data']['authorInfo']['uid']
                comment_info['parent_id']   = 0
                comment_info['root_id']     = data['data']['rootId']
                self.generate_res[content] = comment_info
                #将评论id追加到数组中去
                self.comment_id_arr.append(comment_info['comment_id'])
                return self.comment.index(comment)
            else:
                print('创建动态[ %s ]的评论[%s]失败:)' % (self.feed,comment))
                return None
        except Exception as e:
            print('创建动态[ %s ]的评论出现异常:( %s' % (self.feed,e))
            return None

    # 创建评论的回复
    def create_comment_reply(self,comment,comment_replys):
        for comment_reply in comment_replys:
            #
            content = '%s-%s-%s' % (self.feed,comment,comment_reply)
            params = {
                'feedUid': self.generate_res['uid'],
                'feedId': self.generate_res['feed_id'],
                'type': 2,
                'content': content,
                'parentCommentId' : self.get_parent_or_root_comment_id(self.feed,comment,comment_reply,comment_replys,False),
                'rootCommentId'   : self.get_parent_or_root_comment_id(self.feed,comment,None,None,True),
            }
            try:
                r = requests.post(self.url_create_comment, cookies=self.cookie, data=params)
                if r.status_code == self.ERROR_CODE_OK:
                    data = json.loads(r.text)
                    comment_info = {}
                    comment_info['comment_id']  = data['data']['id']
                    comment_info['comment_uid'] = data['data']['authorInfo']['uid']
                    comment_info['parent_id']   = data['data']['contentInfo']['parentComment']['id']
                    comment_info['root_id']     = data['data']['rootId']
                    # 将评论id追加到数组中去
                    self.comment_reply_id_arr.append(comment_info['comment_id'])
                    #将评论回复添加到数组中去
                    self.generate_res[content] = comment_info
                    print('创建评论[ %s ]回复[ %s ]成功 :)' % (comment,comment_reply))
                else:
                    print('创建评论[ %s ]回复[ %s ] 失败:(' % (comment,comment_reply))
            except Exception as e:
                print('创建[ %s ]回复[ %s ]的时出现异常 :( %s',(comment,comment_reply,e))

    #获取父评论id
    def get_parent_or_root_comment_id(self,feed,comment,reply,replies,isRoot):
        comment_index = '%s-%s' % (feed, comment)
        if isRoot:
            return self.generate_res[comment_index]['comment_id']
        else:
            index = replies.index(reply)
            if index == 0 or isRoot:
                return self.generate_res[comment_index]['comment_id']
            else:
                index = index - 1
                comment_reply = '%s-%s-%s' % (feed,comment,replies[index])
                return self.generate_res[comment_reply]['comment_id']

    # 删除评论
    def delete_comment(self,feed_id,commentId):
        params = {
            'commentId':commentId,
            'feedId':feed_id
        }
        try:
            r = requests.post(self.url_delete_comment,cookies=self.cookie,data=params)
            if r.status_code == self.ERROR_CODE_OK:
                print('删除评论[ %s ]成功:)' % commentId)
                return True
            else:
                print('删除评论[ %s ]失败:(' % commentId)
                return False
        except Exception as e:
            print('删除评论[ %s ]出现异常:( %s' % (commentId,e))
            return False

    #美化输出
    def beautify_output(self,text):
        if text:
            data = json.loads(text)
            print(json.dumps(data,indent=1,ensure_ascii=False))

    #查询评论
    def query_comments(self,feed_id,pageId = 1,pageSize = 10):
        comment_list_query_str = self.url_comment_list % (feed_id, pageId, pageSize)
        ret = False
        print('--------------------------start--------------------------')
        try:
            r = requests.get(comment_list_query_str, cookies=self.cookie)
            if r.status_code == self.ERROR_CODE_OK:
                self.beautify_output(r.text)
                ret = True
            else:
                print('查询动态[ %s ]的第[ %s ]页评论时失败:(' % (feed_id, pageId))
                ret = False
        except Exception as e:
            print('查询动态[ %s ]的第[ %s ]页评论时出现异常 %s:(' % (feed_id, pageId,e))
            ret = False
        print('--------------------------end--------------------------')
        return ret

    #查询评论回复
    def query_comment_replies(self,feed_id,rootId,pageId = 1,pageSize = 10):
        comment_reply_query_str = self.url_comment_reply_list % (feed_id,pageId,pageSize,rootId)
        ret = False
        print('--------------------------start--------------------------')
        try:
            r = requests.get(comment_reply_query_str,cookies=self.cookie)
            if r.status_code == self.ERROR_CODE_OK:
                self.beautify_output(r.text)
                ret = True
            else:
                print('查询评论[ %s ]的第 %s 页回复时失败:(\n%s' % (rootId,pageId,r.text))
                ret = False
        except Exception as e:
            print('查询评论[ %s ]的第 %s 页回复时出现异常 %s:(' % (rootId,pageId,e))
            ret = False
        print('--------------------------end--------------------------')
        return ret

    #打印评论的数目
    def print_comment_count(self,feed_id,comment_ids):
        x = PrettyTable(['type','id','comment_count'])
        x.padding_width = 1
        #动态评论数
        feed_key = '%s%s' % (self.num_comment_query_str, feed_id)
        feed_count = self.redis_count_cli.get(feed_key)
        x.add_row(['动态评论数',feed_id,str(feed_count,encoding='utf-8')])

        for comment_id in comment_ids:
            comment_key   = '%s%s' % (self.num_comment_reply_query_str, comment_id)
            comment_count = self.redis_count_cli.get(comment_key)
            x.add_row(['评论回复数',comment_id,str(comment_count,encoding='utf-8')])
        print(x)

    #将bytes转化为string
    def transfer_byte_to_string(self,b_value):
        if b_value:
            return str(b_value,encoding='utf-8')
        return None

    #查看缓存中的评论信息
    def print_comment_info(self,feed_id):
        comment_id_query_str = '%s%s' % (self.info_comment_id_list_query_str,feed_id)
        comment_ids = self.query_from_redis_db(comment_id_query_str,'zset')
        if comment_ids:
            comment_ids = list(map(self.transfer_byte_to_string,comment_ids))
            print('feed_id为[ %s ]' % (feed_id))
            for comment_id in comment_ids:
                print('\t\t|-----comment_id [%s]' % comment_id)
                comment_reply_query_str = '%s%s' % (self.info_comment_reply_id_list_query_str,comment_id)
                comment_reply_ids = self.query_from_redis_db(comment_reply_query_str,'zset')
                comment_reply_ids = list(map(self.transfer_byte_to_string,comment_reply_ids))
                for comment_reply_id in comment_reply_ids:
                    object_query_str = self.info_comment_obj % comment_reply_id
                    result = self.query_from_redis_db(object_query_str,'string')
                    print('\t\t\t\t|-----reply_id [%s][%s]' % (comment_reply_id, self.transfer_byte_to_string(result)))

    #从db中查找值
    def query_from_redis_db(self,key,type):
        if type == 'zset':
            result = self.redis_info_cli_0.zrange(key,0,-1)
            if result is None:
                return self.redis_info_cli_1.zrange(key,0,-1)
            return result
        elif type == 'string':
            result = self.redis_info_cli_0.get(key)
            if result is None:
                result = self.redis_info_cli_1.get(key)
            return result
        else:
            return None

    #将cookie转化为字典对象
    def transferCookieToDict(self,cookieStr):
        if(self.cookie):
            return self.cookie
        items = cookieStr.split(';')
        for item in items:
            k_v = item.split('=')
            if k_v[0] == '':
                continue
            key   = k_v[0].replace(' ','')
            if len(k_v) == 2:
                value = k_v[1]
            else:
                value = ''
            self.cookie[key] = value
        return self.cookie


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    #查看调用的失败率
    def count_call_failure(self,func,params,times):
        count = times
        total = 0
        fail = 0
        while count:
            ret = func(params)
            total = total + 1
            if ret is False:
                fail = fail + 1
            count = count - 1
        return {times : fail}

    #打印调用失败率
    def print_call_failure_rate(self,method_name,plt_arr):
        x = PrettyTable(['method', 'total', 'fail'])
        x.padding_width = 1
        for key in plt_arr:
            x.add_row([method_name,key,plt_arr[key]])
        print(x)

with AUTO() as auto:
    #先解析一下cookie
    auto.transferCookieToDict(auto.cookieString)
    #创建或者删除评论
    CREATE_HANDLE               = True     #是否创建评论
    DELETE_HANDLE               = False     #是否删除评论(如果CREATE_HANDLE=False时需要手动修改值)
    QUERY_CACHE_HANDLE          = False     #是否查询Cache中的数据
    QUERY_COMMENT_HANDLE        = False     #是否查询评论信息
    QUERY_COMMENT_REPLY_HANDLE  = False      #是否查询评论回复信息
    #
    COUNT_CALL                  = False      #调用统计
    if CREATE_HANDLE:
        #[1]创建评论
        feed_res = auto.create_feed(auto.feed)
        if feed_res:
            cmt_res = map(auto.create_comment,auto.comment)
            for val in cmt_res:
                if val is not None:
                    auto.create_comment_reply(auto.comment[val],auto.comment__reply.get(val + 1))

        print('动态id[ %s ]' % auto.generate_res['feed_id'])
        print('动态评论的id [ %s ]' % auto.comment_id_arr)
        print('评论回复的id [ %s ]' % auto.comment_reply_id_arr)

    if DELETE_HANDLE:
        if CREATE_HANDLE is False:
            feed_id     = 124661
            comment_ids = (122144, 122154, 122164, 122174)
            delete_ids  = (122145, 122146, 122147, 122148, 122149, 122150, 122151, 122152, 122153, 122155, 122156, 122157, 122158, 122159, 122160, 122161, 122162, 122163, 122165, 122166, 122167, 122168, 122169, 122170, 122171, 122172, 122173, 122175, 122176, 122177, 122178, 122179, 122180, 122181, 122182, 122183)
        else:
            feed_id     = auto.generate_res['feed_id']
            comment_ids = auto.comment_id_arr
            delete_ids  = auto.comment_reply_id_arr

        print('删除前')
        auto.print_comment_count(feed_id, comment_ids)
        time.sleep(3)
        #[2]删除评论
        for delete_id in delete_ids:
            print('\n\n\n')
            auto.delete_comment(feed_id,delete_id)
            auto.print_comment_count(feed_id,comment_ids)
            time.sleep(1)

    #[3]查询缓存中的数据
    if QUERY_CACHE_HANDLE:
        auto.print_comment_info(124706)

    #[4]查询评论列表
    if QUERY_COMMENT_HANDLE:
        if CREATE_HANDLE:
            feed_id = auto.generate_res['feed_id']
        else:
            feed_id = 124732
        for index in range(1,3):
            print('第[ %s ]页' % index)
            auto.query_comments(feed_id,index)

    #[5]查询评论的回复
    if QUERY_COMMENT_REPLY_HANDLE:
        for index in range(1,30):
            print('第[ %s ]页' % index)
            auto.query_comment_replies(124706,122970,index)

    if COUNT_CALL:
        plt_arr = {}
        for index in range(10,50,10):
            ret = auto.count_call_failure(auto.query_comments,124732,index)
            plt_arr[index] = ret[index]

        auto.print_call_failure_rate(auto.query_comments.__name__,plt_arr)

