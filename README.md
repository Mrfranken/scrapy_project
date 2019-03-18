# scrapy_project
---
### 20190317

- 建立bole_scrapy工程
- 开始编写jobbole的爬虫
    - 怎样建立一个main文件，通过运行这个文件可以使用pycharm单步调试程序
    - spider开始运行时是从哪个入口开始是什么（start_requests）
    - 使用Request对不同的url进行请求并交给不同的回调函数


### 20190318

- 在Request中使用meta进行额外参数的传递
- 定义Item并在spider中引入，然后yield给Pipeline 