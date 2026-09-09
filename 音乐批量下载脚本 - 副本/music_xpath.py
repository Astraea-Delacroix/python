import tkinter as tk
import webbrowser
import requests
from lxml import etree


class Music():

    def __init__(self):
        self.w = 500
        self.h = 500
        self.title = '阳明-网易云VIP音乐下载助手'
        # 窗口取名
        self.root = tk.Tk(className=self.title)
        # 定义button控件上的文字
        self.url = tk.StringVar()
        # 选择代理
        self.v = tk.IntVar()
        # 默认不使用
        self.v.set(1)
        # Frame空间
        frame_1 = tk.Frame(self.root)
        frame_2 = tk.Frame(self.root)
        frame_3 = tk.Frame(self.root)

        # Menu菜单
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        mp4menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='友情链接', menu=mp4menu)

        # 各个短视频网站链接，友情合作
        mp4menu.add_command(label='抖音', command=lambda: webbrowser.open('./a.png'))

        # 控件内容设置
        group = tk.Label(frame_1, text='请选择一个代理：', padx=10, pady=10)
        tb1 = tk.Radiobutton(frame_1, text='代理一', variable=self.v, value=1, width=10, height=3)
        tb2 = tk.Radiobutton(frame_1, text='代理二', variable=self.v, value=2, width=10, height=3)
        label1 = tk.Label(frame_2, text="请输入音乐链接：")
        entry = tk.Entry(frame_2, textvariable=self.url, highlightcolor='Fuchsia', highlightthickness=1, width=35)
        label2 = tk.Label(frame_2, text=" ")
        play = tk.Button(frame_2, text="提取", font=('楷体', 12), fg='Purple', width=2, height=1, command=self.run)
        label3 = tk.Label(frame_2, text=" ")
        label_explain = tk.Label(frame_3, fg='red', font=('楷体', 12),
                                 text='\n网易云VIP音乐下载！\n注意：此软件仅用于交流学习，请勿用于任何商业用途！')
        label_warning = tk.Label(frame_3, fg='blue', font=('楷体', 12), text='\n音乐将会保存在当前程序文件目录下<muc>\n')

        # 控件布局
        frame_1.pack()
        frame_2.pack()
        frame_3.pack()
        group.grid(row=0, column=0)
        tb1.grid(row=0, column=1)
        tb2.grid(row=0, column=2)
        label1.grid(row=0, column=0)
        entry.grid(row=0, column=1)
        label2.grid(row=0, column=2)
        play.grid(row=0, column=3, ipadx=10, ipady=10)
        label3.grid(row=0, column=4)
        label_explain.grid(row=1, column=0)
        label_warning.grid(row=2, column=0)
    def music_spider(self):

        # 模拟浏览器
        headers = { 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}

        url = self.url.get().replace('/#','')
        # 发送请求
        data = requests.get(url, headers=headers).content.decode()
        html = etree.HTML(data)
        music_url = html.xpath('//ul[@class="f-hide"]/li/a/@href')

        name = html.xpath('//ul[@class="f-hide"]/li/a/text()')

        for i, url in enumerate(music_url):
            new_url = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(url[9:])
            data = requests.get(new_url, headers=headers).content
            file_path = 'muc/' + name[i] + '.mp3'
            with open(file_path, 'wb')as f:
                f.write(data)
                print('{}--已破解'.format(name[i]))

    def run(self):
        dd.music_spider()

    def loop(self):
        self.root.mainloop()

if __name__ == '__main__':
    dd = Music()
    dd.loop()