import segno
from segno import helpers

# 这里改成你想要扫码显示的文字！
text = "妈妈，520快乐呀❤️ 永远爱你"

# 生成纯文本二维码
qr = segno.make(text)

# 保存图片到当前文件夹
qr.save("爱心告白二维码.png", scale=8)

# 直接在窗口显示二维码
qr.show()