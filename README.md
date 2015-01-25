# shanbayAddWords
扇贝批量填词到词库
扇贝还是很不错的背单词系统，但是我一直不理解为什么官方提供的批量添加单词页面每次限制10个= =。 美剧党随手挤了很多单词准备导入的时候，还有从有道单词本导入的时候，都很尴尬。。查了一下，还没有人写过这方面的东西，所以尝试着用python写了个。
下载地址：http://pan.baidu.com/s/1bn93yft


　　
基本思路：
1.请求用户授权
2.循环查词 获取词的ID
3.循环添加到词库 （需要词的ID）

功能很简单，思路也很清晰，但是第一次接触有关API的东西还是有点无从下手，于是看到了廖雪峰写过的一个新浪微博API的小demo，理解了具体的原理。

A.关于获取用户授权
A.1 设置参数
demo创建了一个类叫做APIclient来集成了各种属性，和各种get post方法的源头，方便使用。
其中几个重要的参数都可以简单的搞定，比如app_key secret redirect_url  然后给用户生成一个固定的引导授权地址。
A.2  获取code
当用户授权后，系统会自动根据回调地址回调code参数，如果设置成扇贝默认的回调地址，code部分直接显示在url中，让用户copy回来给我就好了。。虽然不够友好，但是也只能这样了，毕竟要想自动的接收，最开始就要用python调用浏览器来打开这个授权网页，这个感觉好像很麻烦。。
A.3 根据code生成token。
这个也直接写在类里了，不过很简单，按照文档就一步，之后的所有操作都是根据token来和服务器进行身份识别的，所以很重要，而且每一步都要确认token是否过期。

B.get查词
这个就很简单了，不多说，主要的亮点是json的数据格式很好，import json之后，系统自动处理为dict类型，特别方便调用。
C.post填词
更简单，但是要判断是否添加成功，毕竟不是每个词都在词库里记录了。

D.界面
tkinter 还是比较方便吧 但是在win和mac下尺寸不好调成一致，还有mac下输入框中文不能输入很闹心。如果哪一天出现了和vs搞winform那么简单无脑的IDE 我大概就离不开python了~ 

E.
也同时了解到了一个比较惊艳的python高级技巧，郁闷的是我不知道这个东西学名叫什么，从功能上来说，它实现了动态解析函数名的作用。
比如：
bdc_body = client.get.bdc__search(word=w)
这里的client.get 是这样的
def __getattr__(self, attr):
    def wrap(**kw):
        if self.client.is_expires():
            raise APIError('21327', 'expired_token', attr)

        url = '%s%s/' % (self.client.api_url, attr.replace('__', '/'))
        #print(url)
        return _http_call(url, self.method, self.client.access_token, **kw)
    return wrap
它以「__」作为分节符把函数名中的bdc和search作为字符串处理添加到了url中，把参数word=w当做attr字典传入，进行调用http_call去进行连接。 这里完全把函数当做一个变量来处理，可以返回，这样的操作使语言十分简洁，漂亮~~


