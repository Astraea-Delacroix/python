import segno
# 核心参数优化：提高容错率、指定版本、放大尺寸
# 容错率H最高，适配微信弱识别场景；scale放大像素避免模糊
qrcode = segno.make("弑神天刃大傻逼", error="H", version=7)
qrcode.save("qrcode.png", scale=10, border=2)