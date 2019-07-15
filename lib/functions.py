from PIL import Image, ImageTk
import os
import sys

def getImg(root, img_path, width, height):
    img = Image.open(resource_path(img_path))
    resize_img = img.resize((width, height))
    tkimg = ImageTk.PhotoImage(resize_img, master = root)
    return tkimg

def resource_path(relative):
  if hasattr(sys, "_MEIPASS"):
      return os.path.join(sys._MEIPASS, relative)
  return os.path.join(relative)

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

def getQualityNumber(quality):
    if "1080" in quality:
        return 137
    if "720" in quality:
        return 136
    if "480" in quality:
        return 135
    if "360" in quality:
        return 134
    if "240" in quality:
        return 133
    if "144" in quality:
        return 160
