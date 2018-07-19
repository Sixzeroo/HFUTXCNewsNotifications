# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os
import datetime,time
import re,json

from config import Infos, STUDENT_ID, STUDENT_PASSWD,RECEIVERS
from log import logger
from Semail import Email
from Student import Stu


class Info(object):

    def __init__(self,url,key,receivers,name):
        '''
        从文件中读取信息进行初始化
        '''
        self.url=url
        self.key=key
        self.receivers=receivers
        self.name=name
        filename = self.name + "_data.json"
        try:
            with open(os.path.join(os.getcwd(),filename) )as f:
                data=json.load(f)
                self.list=data['list']
                self.update=data['update']
        except FileNotFoundError as e:
            #Todo: 无法加入中文的日志信息
            logger.info('create data file: %s'%filename)
            self.list=[]
            #self.update=int((datetime.date.today()-datetime.timedelta(mounth=1)).strftime("%Y%m%d"))
            self.update=0
            self.save_date()


    def save_date(self):
        '''
        将数据保存到json文件中
        :return: 
        '''
        filename=self.name+"_data.json"
        data = {'list': self.list, 'update': self.update}
        with open(os.path.join(os.getcwd(),filename), 'w') as f:
            json.dump(data,f)



    def get_list(self,url,id=1):
        '''
        根据url获得页面通知的列表，对所有官网的通知界面都有效
        :param url: 页面url,默认页码id为1
        :return: {"name","date","href"}字典
        '''
        base_url=url
        url=url+"/list%s.htm"%id
        Html=requests.get(url=url).content
        soup=BeautifulSoup(Html,'html5lib')
        list=soup.find_all(class_="articlelist2_tr")
        items=[]
        key_re=re.compile(r'^/([0-9a-z]*)/([0-9a-z]*)/([0-9a-z]*)/')
        for item in list:
            tbody=item.find_all("tbody")
            #对于不同的表格格式进行处理
            if(len(tbody)!=0):
                row=tbody[0].find_all("td")
            else:
                row=item.find_all("td")
            name=row[1].find("a").text.strip()
            #将日期转化成int，便于排序
            date=''.join(row[2].text.strip().split('-'))
            #增加时间精度
            date=date+datetime.datetime.now().strftime("%H%M")
            date=int(date)
            href=row[1].find("a").get("href")
            #通过url获得查询的主键
            key=None if re.match(key_re,href) is None else "".join(re.match(key_re,href).group(1,2,3))
            href=base_url+href
            new_item={"name":name,"date":date,"href":href,"key":key}
            #print(new_item)
            items.append(new_item)
        return items

    def get_update_list(self,lists):
        '''
        给出新的列表，获得多出来的更新的列表，同时自身进行更新
        :param lists: 新爬取的列表
        :return: 更新的信息，这个列表是否都是更新值
        '''
        new_lists=[]
        endflag=0

        for item in lists:
            # 初始化的时候用到的特判
            # 除了时间戳，还要使用到hash值进行判断是否重复
            if(len(self.list)!=0 and ( item['date']<self.update or item['key'] == self.list[-1]['key'])):
                endflag=1
                break
            new_lists.append(item)
        # 加入数据中，并更新值
        for item in new_lists[::-1]:
            self.update = max(self.update, item['date'])
            # Todo: 无法加入中文的日志信息
            self.list.append(item)
            logger.info("update item key: %s data: %s" % (item['key'], item['date']))

        return new_lists,endflag


    def filter_keyword(self,new_lists,key):
        '''
        查询相应符合关键字的信息，返回信息列表
        :param new_lists: 更新的新闻
        :param key: re正则表达式
        :return: 符合正则的新闻
        '''
        important_infos=[]
        for item in new_lists:
            ret=key.findall(item['name'])
            if len(ret)==0: continue
            logger.info('Find new filter info key: %s date:%s'%(item['key'],item['date']))
            important_infos.append(item)
        return important_infos

    def send_email_new(self,imp_lists):
        '''
        将重要信息发送邮件给指定联系人
        :param imp_lists: 
        :return: 
        '''
        for item in imp_lists:
            e = Email()
            title = "关于网站新内容更新的通知"
            content = '你好！\n' \
                      '  您感兴趣的网站有新的内容更新：\n' \
                      '  %s\n' \
                      '  %s\n\n\n' \
                      '本邮件由热心人Sixzeroo自动发送，联系方式QQ：1790798600' %(item['name'],item['href'])
            try:
                e.send_email(self.receivers,content,title)
                logger.info('successful send email to %s etc'%self.receivers[0])
            except Exception as e:
                logger.error('When it send email,there are error: %s'%e)

    def work(self):
        # try:
        infos=self.get_list(self.url)
        update_infos,endflag=self.get_update_list(infos)
        fil_infos=self.filter_keyword(update_infos,self.key)
        self.send_email_new(fil_infos)
        logger.info('successful work !')
        self.save_date()
        # except Exception as e:
        #     logger.error('There is a error when work:%s'%e)

class Info2(object):

    def __init__(self, receivers):
        self.stu = Stu(STUDENT_ID, STUDENT_PASSWD)
        self.receivers = receivers
        self.filename = 'stu_achi_data.json'
        try:
            with open(os.path.join(os.getcwd(),self.filename) )as f:
                data=json.load(f)
                self.list=data['list']
                self.update=data['update']
        except FileNotFoundError as e:
            logger.info('create data file: %s'%self.filename)
            self.list=[]
            self.update=0
            self.save_date()


    def save_date(self):
        '''
        将数据保存到json文件中
        :return: 
        '''
        data = {'list': self.list, 'update': self.update}
        with open(os.path.join(os.getcwd(),self.filename), 'w') as f:
            json.dump(data,f)

    def compare(self):
        '''
        对比两次情况，并更新list
        :return: 返回多出来的部分
        '''
        new_list = self.stu.get_achievement()
        ht = {}
        for old_item in self.list:
            ht[old_item['key']] = old_item['course_name']
        # 判断是否有新的
        res_list = []
        for new_item in new_list:
            if(new_item['key'] not in ht):
                res_list.append(new_item)
        self.list = new_list
        return res_list

    def send_email_new(self,diff_lists):
        '''
        将重要信息发送邮件给指定联系人
        :param imp_lists: 
        :return: 
        '''
        e = Email()
        email_content = ''
        for item in diff_lists:
            email_content = email_content + item['course_name'] + '\n'
        title = "关于成绩更新的通知"
        content = '你好！\n' \
                  '  下列课程成绩已出，请注意查询：\n' \
                  '  %s\n\n\n' \
                  '本邮件由热心人Sixzeroo自动发送，联系方式QQ：1790798600' %(email_content)
        try:
            e.send_email(self.receivers,content,title)
            logger.info('successful send email to %s etc'%self.receivers[0])
        except Exception as e:
            logger.error('When it send email,there are error: %s'%e)

    def work(self):
        diff = self.compare()
        if(len(diff) != 0):
            self.send_email_new(diff)
        self.save_date()



if __name__ == '__main__':
    # for item in Infos:
    #     info = Info(item['url'],item['re_key'],item['receivers'],item['name'])
    #     info.work()
    instance = Info2(RECEIVERS)
    instance.work()

