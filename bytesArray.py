class BytesArray:
    def __init__(self):
        self.intData = []
        self.bytesData = []

    def initFile(self, filename=None):
        self.filename = filename
        self.intData = []
        self.bytesData = []
        with open(filename, "rb") as f:
            for i in f.read():
                self.bytesData.append(bytes([i]))
                self.intData.append(i)
        return self

    def initString(self, string, encoding):
        self.intData = []
        self.bytesData = []
        string = bytes(string, encoding)
        for i in string:
            self.bytesData.append(bytes([i]))
            self.intData.append(i)
        return self

    def initBytes(self, byte):
        self.intData = []
        self.bytesData = []
        for i in byte:
            self.intData.append(i)
            self.bytesData.append(bytes([i]))
        return self

    def initInt(self, value, length):
        self.intData = []
        self.bytesData = []
        bytes_value = value.to_bytes(length, byteorder='big')
        for i in bytes_value:
            self.intData.append(i)
            self.bytesData.append(bytes([i]))
        return self

    def setBit(self, index, offset, value):
        if self.intData[index] & (2 ** offset) == 2 ** offset and not value:  # offset位为1且欲将其置0
            self.intData[index] -= 2 ** offset
        elif self.intData[index] & (2 ** offset) != 2 ** offset and value:  # offset位为0且欲将其置1
            self.intData[index] += 2 ** offset
        self.bytesData[index] = bytes([self.intData[index]])

    def setBitByOffset(self, offset, value):
        index = int(offset / 8)
        offset = offset % 8
        self.setBit(index, offset, value)

    def getBit(self, index, offset):
        return self.intData[index] & (2 ** offset) == 2 ** offset;

    def getBitByOffset(self, offset):
        index = int(offset / 8)
        offset = offset % 8
        return self.getBit(index, offset)

    def toBytes(self):
        Bytes = b''
        for i in self.bytesData:
            Bytes += i
        return Bytes

    def writeToFile(self, filename):
        originData = b''
        for i in self.bytesData:
            originData += i
        with open(filename, 'wb') as f:
            f.write(originData)
