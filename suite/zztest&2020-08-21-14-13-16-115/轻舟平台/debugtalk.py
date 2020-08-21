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

def getbusiness_id():
    db = MySQLdb.connect("10.128.138.240", "cloudwalk", "1qaz!QAZ", "cwos-portal", charset='utf8' )
    with db:
    cursor1 = con.cursor()
    cursor1.execute("select ID from cw_ac_business where CORP_CODE='chuangxin'")
    data1 = cursor1.fetchall()
    
    print data1
    return data1
    
def getareaId(data):
    db = MySQLdb.connect("10.128.138.240", "cloudwalk", "1qaz!QAZ", "cwos-portal", charset='utf8' )
    with db:
    cursor2 = con.cursor()
    cursor2.execute("select * from cw_is_area where `NAME`='区位_a' and BUSINESS_ID='%s'"% data)
    data2 = cursor2.fetchall()
    
    print data2
    return data2


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
