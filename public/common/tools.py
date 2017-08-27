#-*- coding:utf-8 -*-
import IPy
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

def exchange_maskint(mask_int):
    bin_arr = ['0' for i in range(32)]
    for i in range(mask_int):
        bin_arr[i] = '1'
    tmpmask = [''.join(bin_arr[i * 8:i * 8 + 8]) for i in range(4)]
    tmpmask = [str(int(tmpstr, 2)) for tmpstr in tmpmask]
    return '.'.join(tmpmask)

def check_ip(ip):
    list = ip.split('.')
    if len(list) != 4:
        return False
    for i in list:
        if i.isdigit() == True and int(i) >= 0 and int(i) <= 255:
            pass
        else:
            return False
    return True

def get_segment_by_ip_mask(ip, mask):
    if not check_ip(ip):
        return False, 'ip不合法'
    if not check_ip(mask):
        return False, '网关错误'
    return True, str(IPy.IP(ip).make_net(mask))

def get_maskint_by_segment(segment):
    segment_arr = segment.split("/")
    if len(segment_arr) != 2:
        return False
    if not check_ip(segment_arr[0]):
        return False
    if not str(segment_arr[1]).isdigit():
        return False
    maskint = int(str(segment_arr[1]))
    if maskint < 0 or maskint > 32:
        return False
    return maskint

class Prpcrypt():

    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    #加密函数，如果text不足16位就用空格补足为16位，
    #如果大于16当时不是16的倍数，那就补足为16的倍数。
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        #这里密钥key 长度必须为16（AES-128）,
        #24（AES-192）,或者32 （AES-256）Bytes 长度
        #目前AES-128 足够目前使用
        length = 16
        count = len(text)
        if count < length:
            add = (length-count)
            text = text + ('\0' * add)
        elif count > length:
            add = (length-(count % length))
            text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        return b2a_hex(self.ciphertext)

    #解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        plain_text  = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')