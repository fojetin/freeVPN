'''
HACK Seed4.me with temp-mail.org
'''
import requests
from urllib.parse import unquote
from bs4 import BeautifulSoup
from time import sleep


tmp_session = requests.session()
def get_temp_mail(tmp_session):
    temp_mail_resp = tmp_session.get('https://temp-mail.org/')
    encode_temp_mail = temp_mail_resp.cookies.get('mail')
    mail = unquote(encode_temp_mail)
    return mail


if __name__ == '__main__':
    mail = get_temp_mail(tmp_session)
    password = mail[:mail.index('@')]
    seed4me_session = requests.session()
    reg_data = {
        '_method': 'POST',
        'data[User][username]': mail,
        'data[User][password]': password,
        'data[User][confirmPassword]': password,
        'data[User][promoCode]': '',
        'data[User][accept]': 'N',
        'data[User][accept]': 'yes',
    }
    seed_resp = seed4me_session.post('https://seed4.me/users/register', data=reg_data)
    sleep(5)
    temp_mails = tmp_session.get('https://temp-mail.org/en/option/refresh/')
    temp_mails_soup = BeautifulSoup(temp_mails.text)
    tmp_link = temp_mails_soup.find('a', {'title': 'Welcome to Seed4.Me - Private VPN Club.'}).get('href')
    confirm_mail = tmp_session.get(tmp_link)
    confirm_mail_soup = BeautifulSoup(confirm_mail.text)
    confirm_link = confirm_mail_soup.find('a', {'title':'CONFIRM YOUR EMAIL'}).get('href')
    seed4me_session.get(confirm_link)

    print('Successfully received a free vpn for a week!')
    print('Login:', mail)
    print('Password:', password)