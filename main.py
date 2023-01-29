import requests, json, time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

class Book:
    def __init__(self) -> None:
        self.cookies = {
            '_ga': 'GA1.2.1721389846.1649773321',
            'token': 'Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJCQkRDIiwiTlJJQyI6IlM4OTU1OTYzRCIsImV4cCI6MTY3Mzk3MTY2Nn0.-zoev2Cv5rMM7ZTkOh1o5x-0SmSxv6i4SIz-l8YXtOI',
        }

        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJCQkRDIiwiTlJJQyI6IlM4OTU1OTYzRCIsImV4cCI6MTY3Mzk3MTY2Nn0.-zoev2Cv5rMM7ZTkOh1o5x-0SmSxv6i4SIz-l8YXtOI',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            # Requests sorts cookies= alphabetically
            # 'Cookie': '_ga=GA1.2.1721389846.1649773321; bbdc-token=Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJCQkRDIiwiTlJJQyI6IlM4OTU1OTYzRCIsImV4cCI6MTY3Mzk3MTY2Nn0.-zoev2Cv5rMM7ZTkOh1o5x-0SmSxv6i4SIz-l8YXtOI',
            'JSESSIONID': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJBQ0NfSUQiOiI5ODY4NDQiLCJpc3MiOiJCQkRDIiwiTlJJQyI6IlM4OTU1OTYzRCIsImV4cCI6MTMwNTIyOTA0MDg2fQ.o46RgxiaXsIW9tW_CCPxIBXPFU-h7I-3KUDpu2F1y98',
            'Origin': 'https://booking.abc.sg',
            'Referer': 'https://booking.abc.sg/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }
    
    def query(self):
        json_data = {
            'subStageSubNo': None,
            'insInstructorId': '',
        }

        response = requests.post('https://booking.abc.sg/abc-back-service/api/booking/c3practical/listC3PracticalSlotReleased', cookies=self.cookies, headers=self.headers, json=json_data)
        return response
    
    def book(self, slotList):
        json_data = {
            'courseType': '123',
            'insInstructorId': '',
            'subVehicleType': None,
            'slotIdList': slotList,
        }
        response = requests.post('https://booking.abc.sg/abc-back-service/api/booking/c3practical/callBookC3PracticalSlot', cookies=self.cookies, headers=self.headers, json=json_data)
        return response
    
    def getSlotList(self, response):
        slotList = []
        
        if response == None or response.content == None:
            return False
        j = json.loads(response.content)

        if 'data' in j and 'releasedSlotListGroupByDay' in j['data'] and j['data']['releasedSlotListGroupByDay'] != None:
            for k, v in j['data']['releasedSlotListGroupByDay'].items():
                if len(v) > 0 and v[0]['c3PsrFixGrpNo'] == "G6067":
                    slotList.append(v[0]['slotId'])
            
            if len(slotList) == 0:
                return False
            
            return slotList
        else:
            print("no slot")
            return False
        
    def sendEmail(self):
        sender = '12345678@qq.com' # 你的发送方Email地址
        receivers = ['codingxiaoma@gmail.com']  # 你的接收方Email地址
        
        message = MIMEText('预约成功', 'plain', 'utf-8')
        message['From'] = Header("预约", 'utf-8')
        message['To'] =  Header("预约", 'utf-8')
        
        subject = '预约成功'
        message['Subject'] = Header(subject, 'utf-8')
        
        
        try:
            smtpObj = smtplib.SMTP() 
            smtpObj.connect('smtp.qq.com', 587)  # SMTP邮件服务器
            smtpObj.login(sender,'jejkgpxxotttcacb')  # 发送方的邮箱和密码/授权码，腾讯邮箱可以在账户设置里面开启POP3/SMTP服务器并得到一个授权码
            smtpObj.sendmail(sender, receivers, message.as_string())
            print ("邮件发送成功")
        except smtplib.SMTPException:
            print ("Error: 无法发送邮件")

if __name__ == "__main__":
    a = Book()
    
    while True:
        res = a.query()
        slotList = a.getSlotList(res)
        if slotList == False:
            print("no slot, try again")
        else:
            a.book(slotList)
            a.sendEmail()

        time.Sleep(5)