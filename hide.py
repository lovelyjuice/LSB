from bytesArray import BytesArray

from PIL import Image

if __name__ == "__main__":
    imgPath = input('BMP位图路径：')
    secretPath = input('需要隐藏的文件的路径：')
    savePath = input('隐写后的图片保存在：')
    baseImg = Image.open(imgPath)
    secret = BytesArray().initFile(secretPath)
    secretSize = secret.bytesData.__len__() * 8
    print(secretSize)
    header = BytesArray().initInt(secretSize, 6)
    width, height = baseImg.size
    num = 0
    x = 0
    y = 0
    for y in range(height):
        for x in range(width):
            if y * height + x >= 16:
                break
            r, g, b = baseImg.getpixel((x, y))
            mod = BytesArray().initInt(r, 1)
            mod.setBit(0, 0, True) if header.getBitByOffset(num) else mod.setBit(0, 0, False)
            r = mod.intData[0]
            num += 1
            mod = BytesArray().initInt(g, 1)
            mod.setBit(0, 0, True) if header.getBitByOffset(num) else mod.setBit(0, 0, False)
            g = mod.intData[0]
            num += 1
            mod = BytesArray().initInt(b, 1)
            mod.setBit(0, 0, True) if header.getBitByOffset(num) else mod.setBit(0, 0, False)
            b = mod.intData[0]
            num += 1
            baseImg.putpixel((x, y), (r, g, b))
        else:
            continue
        break
    num = 0
    print(x, y)
    while y < height:
        while x < width:
            if num >= secretSize:
                break
            r, g, b = baseImg.getpixel((x, y))
            mod = BytesArray().initInt(r, 1)
            mod.setBit(0, 0, True) if secret.getBitByOffset(num) else mod.setBit(0, 0, False)
            r = mod.intData[0]
            num += 1
            if num >= secretSize:
                break
            mod = BytesArray().initInt(g, 1)
            mod.setBit(0, 0, True) if secret.getBitByOffset(num) else mod.setBit(0, 0, False)
            g = mod.intData[0]
            num += 1
            if num >= secretSize:
                break
            mod = BytesArray().initInt(b, 1)
            mod.setBit(0, 0, True) if secret.getBitByOffset(num) else mod.setBit(0, 0, False)
            b = mod.intData[0]
            num += 1
            baseImg.putpixel((x, y), (r, g, b))
            x += 1
        else:
            x = 0
            y += 1
            continue
        break
    baseImg.save(savePath)
