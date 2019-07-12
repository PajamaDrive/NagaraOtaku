from PIL import Image, ImageTk

def getImg(root, img_path, width, height):
    img = Image.open(img_path)
    resize_img = img.resize((width, height))
    tkimg = ImageTk.PhotoImage(resize_img, master = root)
    return tkimg

def getQuality(quality):
    quality_str = []
    if "137" in quality:
        quality_str.append("1080p")
    if "136" in quality:
        quality_str.append("720p")
    if "135" in quality:
        quality_str.append("480p")
    if "134" in quality:
        quality_str.append("360p")
    if "133" in quality:
        quality_str.append("240p")
    if "160" in quality:
        quality_str.append("144p")
    return quality_str
