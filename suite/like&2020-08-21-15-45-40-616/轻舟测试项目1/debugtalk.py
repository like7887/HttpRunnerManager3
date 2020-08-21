# debugtalk.py
import redis
import MySQLdb

def getVerifyCode(captchaKey):
    red = redis.StrictRedis(host="10.128.138.240", password="1qaz!QAZ", db=1)
    verifyCode = red.get("VerifyCaptcha:" + captchaKey).decode() if red.exists("VerifyCaptcha:" + captchaKey) else ""
    return verifyCode



def testGet():
    return "4rcd"
    

def getMysqlVersion():
    db = MySQLdb.connect("10.128.138.240", "cloudwalk", "1qaz!QAZ", "cwos-portal", charset='utf8' )
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()

    print("Database version : %s " % data)
    db.close()

#设备ak，as做AES加密
def aes_encrypt(text):
    BS = len("cloudwalk2018!@#")
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    key = 'cloudwalk2018!@#'.encode('utf-8')
    mode = AES.MODE_ECB
    cryptos = AES.new(key, mode)
    cipher_text = cryptos.encrypt(bytes(pad(text), encoding="utf8"))
    result = b2a_hex(cipher_text).decode()
    return str(result).upper()
    
##图片转base64
def PicToBase64(picPath):
    f = open(picPath , "rb")
    base64data = base64.b64encode(f.read())
    f.close()
    return base64data.decode()
