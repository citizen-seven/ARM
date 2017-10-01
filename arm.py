import vk_api
import time
import random

def captcha_handler(captcha):
    print(captcha.get_url())
    key = input("Enter captcha code: ").strip()
    return captcha.try_again(key)

login, password = 'YOUR_LOGIN_HERE', 'YOUR_PASSWORD_HERE'
user = vk_api.VkApi(login, password,
        captcha_handler = captcha_handler
    )
user.auth()

def write_msg(user_id, s):
    user.method('messages.send', {'user_id':user_id,'message':s})

msgs = [u'Привет! Я редко бываю онлайн. Для связи по срочным вопросам можешь написать в телеграм t.me/eltsin или на почту iskhakov.ra@phystech.edu',
        u'Спасибо за сообщение! Я обязательно прочту его в ближайшее время. Если вопрос срочный, напиши в телеграм t.me/eltsin или отправь e-mail: iskhakov.ra@phystech.edu',
        'Hi! I`m offline now. In case of urgent messages, please, use Telegram (t.me/eltsin) or e-mail me at iskhakov.ra@phystech.edu']
repeats = [u'Если срочно, смотри предыдущее сообщение.',
         u'Это бот и любые попытки тщетны. Он еще маленький и только учится разговаривать с людьми :)',
         u'Обычно Ришат заходит по вечерам, подожди чуток.',
         u'Терпение, Ришат заходит сюда редко, но всегда всем отвечает.']

values = {'count': 100, 'time_offset': 1000}
IDs = set()
to_answer = set()

while True:
    response = user.method('messages.get', values)
    if response['items']:
        values['last_message_id'] = response['items'][0]['id']
        for item in response['items']:
            if not('chat_id' in item.keys()) and not((item['read_state'])):
                ID = item[u'user_id']
                to_answer.add(ID)
                print(item['body'])
    for ID in to_answer:
        if (ID in IDs):
            repeat = random.randint(0,3)
            write_msg(ID, repeats[repeat])
        else:
            IDs.add(ID)
            if (len(IDs) > 20):
                IDs.pop()
            msg = random.randint(0,2)
            write_msg(ID, msgs[msg])
    time.sleep(60)
    to_answer.clear()
