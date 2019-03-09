#!/usr/bin/env python3
# pip3 install zxing

import zxing
reader = zxing.BarCodeReader()
qrcode = reader.decode("QRcode2.jpg")
print(qrcode.parsed)
