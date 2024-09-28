from PIL import Image

# 打开原始图像
img = Image.open("static/reply_bg.png")

# 重新保存图像，消除警告
img.save("static/reply_bg.png", "PNG")
print("Image saved successfully!")