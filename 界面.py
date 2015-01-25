__author__ = 'Lin'
import  Main
from tkinter import*
from tkinter.messagebox import *
import  time

APP_KEY = "a40e6b12f395da55a88b"
APP_SECRET = "5feaab8faecb3cab596fb9808e1c8b7b61ac78c1"
CALLBACK_URL = 'https://api.shanbay.com/oauth2/auth/success/'
#step 2 引导用户到授权地址
client = Main.APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
isLogin = False


root=Tk(className=' 批量填词')
root.geometry('723x525+320+95')


def login():
    Login_window=Toplevel(root)
    Login_window.title('Login')
    Login_window.geometry('520x205+420+200')
    login_contain=Text(Login_window,width=70,height=4,bd=4)
    login_contain.grid(row=1,column=0,rowspan=25)

    label_1=Label(Login_window,text='请复制这个连接到浏览器打开: ',width=70)
    label_1.grid(row=0,column=0)

    label_2=Label(Login_window,text='将授权后所转到的页面的链接中的http://...../?code=后面的部分复制到下面: ',width=70)
    label_2.grid(row=60,column=0)
    label_3=Label(Login_window,text='例如：6wlWvz0sIZKo2ngfsoY9tf3Nn6v1pt',width=70)
    label_3.grid(row=90,column=0)

    code = StringVar()
    codeEn=Entry(Login_window,width=70,textvariable = code)
    codeEn.grid(row=120,column=0)

    # try:
    #step 1 定义 app key，app secret，回调地址：

    login_url = client.get_authorize_url()
    login_contain.insert(END,login_url)
    def Finish():
        global isLogin
        c = code.get()
        l = len('6wlWvz0sIZKo2ngfsoY9tf3Nn6v1pt')
        if(len(c)!=l):
            showinfo('Code Error','code的长度不对，重新复制试试。')
        else:
            r = client.request_access_token(c)#输入授权地址中获得的CODE
            client.set_access_token(r.access_token, r.expires_in) #get tokens
            acc = client.get.account()
            nickname = acc['nickname']
            welstr = '登录成功 %s ! 可以开始填词了，请在下面的文本框中输入单词，每行一个，尽量一次不要太多。'%(nickname)
            showinfo('Okay!',welstr)
            isLogin = True
            label_wel['text'] = nickname + ',登录成功! '
            print(label_wel['text'])
            Login_window.destroy()
    finish_but=Button(Login_window,bd=3,text='Finish',command=Finish)#comand
    finish_but.grid(row=300,column=0,ipadx=16)
    #step 3 换取Access Token
    #r = client.request_access_token(input("Input code:"))#输入授权地址中获得的CODE

    #print('request ok! ')

    #client.set_access_token(r.access_token, r.expires_in) #get tokens

menu_but_F=Menubutton(root,text='File',underline=0)
menu_but_F.grid(row=0,column=0,ipadx=20)
menu_but_F.menu=Menu(menu_but_F)
menu_but_F.menu.add_command(label='Login',command=login)
menu_but_F.menu.add_command(label='Exit',command=root.destroy)
menu_but_F['menu']=menu_but_F.menu

menu_but_H=Menubutton(root,text='About',underline=0)
menu_but_H.grid(row=0,column=1,ipadx=20)
menu_but_H.menu=Menu(menu_but_H)
menu_but_H.menu.add_command(label='Help',command=(lambda :showinfo('Help','=.= 没什么可写的，照着提示用吧 很简单。')))
menu_but_H.menu.add_command(label='About',command=(lambda :showinfo('About','扇贝批量填词工具 -，- QQ：200975730 邮箱:yuchenlin0212@163.com')))
menu_but_H['menu']=menu_but_H.menu


label_wel=Label(root,text='未登录，请先从 File-->Login 中登录',width=50,height=3)
label_wel.grid(row=1,column=0,columnspan=2,rowspan=3)

text=Text(root,height=30,bd=5)
text.grid(row=10,column=0,columnspan=15,rowspan=7)

def Batch():
    global isLogin
    if(not isLogin):
        showerror('Unlogin','清先登录')
        return
    showinfo("Wait..",'填词开始，可能要等一段时间，关注动态请看py.exe（黑框程序）的进展.')
    words_text = text.get(0.0,END)
    lst = words_text.rstrip().split('\n')
    words = []
    for word in lst:
        if(' ' not in word):
            words.append(word)
    N = len(words)
    count = 0
    failed = []
    for word in words:
        #print(word)
        if(Main.AddWord(client,word)):
            count+=1
        else:
            failed.append(word)
    url = '未收入词汇'+str(time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time())))+'.txt'
    if(len(failed)>0):

        fo = open(url,'w',encoding='utf-8')
        s = ''
        for word in failed:
            s+=word+'\n'
        fo.write(s)
        fo.close()
    showinfo("Result",'你输入的单词一共有%d个，成功添加到词'
                      '库有%d个，未被扇贝收入的词有%d个。这些未被收入的词已经被自动保存到了同目录下的%s文档。'%(N,count,N-count,url))
but_to_sentense=Button(root,bd=3,text='开始填入到词库',command=Batch)
but_to_sentense.grid(row=90,column=35)

sl = Scrollbar(root)
sl.grid(row=10,column=26,sticky='ns',rowspan=7)
text['yscrollcommand'] = sl.set
sl['command'] = text.yview



root.mainloop()
