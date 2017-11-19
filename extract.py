from bytesArray import BytesArray

from PIL import Image

if __name__ == "__main__":
    imgPath = input('BMP位图路径：')
    cntPath = input('提取后的文件位置：')
    hiddenImg = Image.open(imgPath)
    width, height = hiddenImg.size
    header = BytesArray().initInt(0, 6)
    num = 0
    x, y = 0, 0
    for y in range(height):
        for x in range(width):
            if y * height + x >= 16:
                break
            r, g, b = hiddenImg.getpixel((x, y))
            temp = BytesArray().initInt(r, 1)
            header.setBitByOffset(num, True) if temp.getBitByOffset(0) else header.setBitByOffset(num, False)
            num += 1
            temp = BytesArray().initInt(g, 1)
            header.setBitByOffset(num, True) if temp.getBitByOffset(0) else header.setBitByOffset(num, False)
            num += 1
            temp = BytesArray().initInt(b, 1)
            header.setBitByOffset(num, True) if temp.getBitByOffset(0) else header.setBitByOffset(num, False)
            num += 1
        else:
            continue
        break
    mount = int.from_bytes(header.toBytes(), 'big')
    print(mount)
    content = b''
    for i in range(int(mount / 8)):
        content += b'0'
    content = BytesArray().initBytes(content)
    num = 0
    print(x, y)
    while y < height:
        while x < width:
            if num >= mount:
                break
            r, g, b = hiddenImg.getpixel((x, y))
            temp = BytesArray().initInt(r, 1)
            content.setBitByOffset(num, True) if temp.getBitByOffset(0) else content.setBitByOffset(num, False)
            num += 1
            if num >= mount:
                break
            temp = BytesArray().initInt(g, 1)
            content.setBitByOffset(num, True) if temp.getBitByOffset(0) else content.setBitByOffset(num, False)
            num += 1
            if num >= mount:
                break
            temp = BytesArray().initInt(b, 1)
            content.setBitByOffset(num, True) if temp.getBitByOffset(0) else content.setBitByOffset(num, False)
            num += 1
            x += 1
        else:
            y += 1
            x = 0
            continue
        break
    content.writeToFile(cntPath)
