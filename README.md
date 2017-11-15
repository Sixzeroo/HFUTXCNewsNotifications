## 网站通知更新推送

通过定时爬取合肥工业大学宣城校区官网的通知页面，获得更新信息。
通过指定的过滤方案判断是否进行邮件通知

## 使用

### 设置网站监控信息
修改value.py中的信息
```
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
```


### 设置定时信息
在服务器中通过contab设置定时执行启动脚本
