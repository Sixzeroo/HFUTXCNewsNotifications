## 网站通知更新推送

通过定时爬取合肥工业大学宣城校区官网的通知页面或者个人成绩信息，获得更新信息。

## 使用

### 下载项目
```
git clone git@github.com:Sixzeroo/HFUTXCNewsNotifications.git 
```

### 设置配置信息
创建`config.py`配置文件如下：
```
# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import re


#收件人列表
# RECEIVERS=['XXXXXXXXXXXX','XXXXXXXXXXXX','XXXXXXXXXXXX']
RECEIVERS=['XXXXXXXXXXXXX']


# 以站点对监控网站对象信息进行整合
Infos = [
    # 教务处考试相关信息
    {
        'name' : 'xcjwb',
        'url' : 'http://xcjwb.hfut.edu.cn/714',
        're_key' : re.compile(r'周考试安排'),
        'receivers' : RECEIVERS,
    },
    # 主页网站竞赛相关新闻
    {
        'name' : 'mian_match',
        'url' : 'http://xc.hfut.edu.cn/121',
        're_key' : re.compile(r'比赛|放假|大赛|竞赛'),
        'receivers' : RECEIVERS,
    }
]


# 邮件设置
EMAIL_CONFIG={
    #发件人
    'sender':'XXXXXXXXXXXXXX',
    #发件人邮箱
    'sender_mail':'XXXXXXXXXXXXXX',
    #邮箱smtp服务器地址
    'host_server':'smtp.163.com',
    #授权码
    'passwd':'XXXXXXXXXXXx',
    #端口 网易SSL为465，普通为25
    'port':'25',
}

STUDENT_ID = 'XXXXXXXXXX'
STUDENT_PASSWD = 'XXXXXXXXXXX'


LOGGING_CONFIG={
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logging.log',
            'level': 'DEBUG',
            'formatter': 'simple'
        },
    },
    'loggers':{
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG',
            # 'propagate': True,
        },
        'simple': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        }
    }
}
```

### 设置定时信息
编辑`crontabfile`文件配置定时信息

### Docker构建
运行脚本`build_docker.sh`构建Docker镜像

### 启动服务
```
sudo docker-compose up -d
```
