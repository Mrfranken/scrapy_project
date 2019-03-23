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

### 20190320

```
当Item在Spider中被收集之后，它将会被传递到Item Pipeline，一些组件会按照一定的顺序执行对Item的处理。

每个item pipeline组件(有时称之为“Item Pipeline”)是实现了简单方法的Python类。
他们接收到Item并通过它执行一些行为，同时也决定此Item是否继续通过pipeline，或是被丢弃而不再进行处理。
item pipeline的典型应用：
1. 清理HTML数据
2. 验证爬取的数据(检查item包含某些字段)
3. 查重(并丢弃)
4. 将爬取结果保存到数据库中
```
- 当获取当item之后放入item pipeline进行再处理，可以给item的字段进行赋值、修改等
    - e.g. 关于下载图片需要在settings.py文件中定义
    MAGES_URLS_FIELD（item中图片下载url字段）和 IMAGES_STORE 图片存储地址
    - **重写 item_completed 方法**
- 将获得的item以json文件的形式进行存储
    - 可以自定义pipeline进行json的存储
    - 也可以使用 scrapy.exporters.JsonItemExporter进行文件的存储
        - **必须实现 process_item 方法**
```python
class JsonExporterPipeline(object):
"""
1. 使用scrapy原生的json文件到处类进行json文件的写入
2. 与JsonWithEncodingPipeline类功能一致
"""
def __init__(self):
    self.file = open(target_file, 'wb')
    self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
    self.exporter.start_exporting()

def process_item(self, item, spider):
    self.exporter.export_item(item)
    return item

def close_spider(self, spider):
    self.exporter.finish_exporting()
    self.file.close()

```

### 20190321

- 建立工程下载http://yinyuesheng.cn/ukulele/pu/的谱子
- 每首歌对应多张谱子，根据谱子的url对谱子重命名
    - 重写 ImagesPipeline 类中的方法
        - get_media_requests 返回一个含有Request的列表
        - file_path          返回图片下载后的路径，源码中图片的名字为url通过sha1哈希得到: hashlib.sha1(to_bytes(url)).hexdigest() 可在这个方法中对文件名进行修改
        - item_completed     item完成后（应该）调用的最后一个方法，在这里可以最后对item进行一些数据的增、删、改（改好像不行，具体要验证）
        - 三个方法的在类中会被依次调用 get_media_requests -> file_path -> item_completed

### 20190323

- 数据库的操作
    - 方法一：定义一个类 e.g. MysqlPipeline 在类中实现mysql数据库的插入逻辑
    - 方法二：定义一个类 e.g. MysqlTwistedPipline 同时引入twisted库，使用异步的方式对数据库进行数据插入（twisted这部分完全不了解,所谓的异步到底是什么呢）













