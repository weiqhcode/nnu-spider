# nnu-spider

针对南宁学院课表的爬虫，它可以自动登录教务系统，获取指定学期，周的课表。

想要运行这个项目你需要填入一些自己的参数。

```python
user_name = '你的学号'
password = '你的教务系统登录密码'
SecretKey = '百度AI平台SecretKey'
ApiKey = '百度AI平台ApiKey'
```

要使用百度的 API 是因为登录时的验证码需要图文识别。

存储的形式是以 JSON 形式存储到 MongoDB 上。
