import secrets, string, requests, json, ssl, smtplib, re
import base64
import os,pytz
from datetime import datetime
from email.message import EmailMessage
from decouple import config

wa_instance = config('WHATSAPP_INSTANCE')
wa_token = config('WHATSAPP_TOKEN')
current_time = datetime.now(pytz.timezone('Africa/Lusaka')) 

wa_key = config('WA_KEY')
timeoutSeconds = 60

#FUNCTION TO CONVERT MOBILE NUMBER TO 9 DIDGITS
def convert_phone_number(phone):

    # Check if phone contains international values +260 or 260
    if phone.find('+260') != -1:
        newphone = str.replace(phone, '+260', '')
    elif phone.find('+263') != -1:
        newphone = str.replace(phone, '+263', '')
    elif phone.find('260') != -1:
       newphone = str.replace(phone, '260', '')
    elif phone.find('263') != -1:
       newphone = str.replace(phone, '263', '')
    elif phone.find('0') != -1:
        newphone = str.replace(phone, '0', '')
    
  
    # actual pattern which only change this line
    num = re.sub(r'(?<!\S)(\d{3})-', r'(\1) ',  newphone) 
    return num

#FUNCTION TO GENERATE DIGIT CODE
def gen_len_code(length, num_only):

    code = None
    
    if num_only:
        digits = string.digits
        code = ''.join(secrets.choice(digits) for i in range(length))
    else:
        # alphabet = string.ascii_letters + string.digits
        alphabet = string.ascii_uppercase + string.digits
        code = ''.join(secrets.choice(alphabet) for i in range(length))
    return code


#FUNCTION TO SEND WHATSAPP USING GREEN API
def send_wa_GreenAPI(sendto, msg):

    dictionary = {"chatId" : sendto + "@c.us","message": msg}
    jsonString = json.dumps(dictionary, indent=4)

    url = "https://api.green-api.com/waInstance" + wa_instance + "/sendMessage/" + wa_token 

    payload = jsonString
    headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    response  = ""

    try:
        response = requests.request("POST", url, headers=headers, data = payload, timeout=timeoutSeconds)
    except (requests.exceptions.RequestException, ValueError) as e:
        response = e

    return response.text.encode('utf8')


#FUNCTION TO SEND WHATSAPP USING GREEN API
def sendFile_wa_GAPI(sendto, link, caption):

    dictionary = {"chatId" : sendto + "@c.us", "urlFile": link, "fileName": "1.pdf", "caption": caption}

    jsonString = json.dumps(dictionary, indent=4)

    url = "https://api.green-api.com/waInstance" + wa_instance + "/sendFileByUrl/" + wa_token 
    payload = jsonString
    headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    response  = ""

    try:
        response = requests.request("POST", url, headers = headers, data = payload, timeout=timeoutSeconds)
    except (requests.exceptions.RequestException, ValueError) as e:
        response = e
    
    return response.text.encode('utf8')


#FUNCTION TO SEND WHATSAPP USING GREEN API
def sendFile_wa_GAPI_group(sendto, msg):

    created_date = current_time.strftime('%Y%m%d%H%M%S')
    dictionary = {"chatId" : sendto + "@g.us", "urlFile": msg, "fileName":"1.pdf", "caption": 'Hi Team please find Sermon study notes for this week. Please read through and let us meet on wednesday'}

    jsonString = json.dumps(dictionary, indent=4)

    url = "https://api.green-api.com/waInstance" + wa_instance + "/sendFileByUrl/" + wa_token 

    payload = jsonString
    headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    response  = ""

    try:
        response = requests.request("POST", url, headers = headers, data = payload, timeout=timeoutSeconds)
    except (requests.exceptions.RequestException, ValueError) as e:
        response = e

    return response.text.encode('utf8')


#FUNCTION TO SEND WHATSAPP BUTTONS USING GREEN API
def sendBtn_GAPI(sendto, msg, yesURL, noURL):

    dictionary = {  "chatId" : sendto + "@c.us", 
                    "message": msg,
                    "footer": "Please choose answer by clicking a button?",
                    "templateButtons": [
                            {"index": 1, "urlButton": {"displayText": "Yes I managed", "url": yesURL}},
                            {"index": 2, "urlButton": {"displayText": "No I did not manage", "url": noURL}}
                        ]
                 }

    jsonString = json.dumps(dictionary, indent=4)

    url = "https://api.green-api.com/waInstance" + wa_instance + "/sendTemplateButtons/" + wa_token 

    payload = jsonString
    headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    response  = ""

    try:
        response = requests.request("POST", url, headers = headers, data = payload, timeout=timeoutSeconds)
    except (requests.exceptions.RequestException, ValueError) as e:
        response = e
    
    return response.text.encode('utf8')



   