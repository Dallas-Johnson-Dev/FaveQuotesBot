import requests
import os
import botcommand
import pickle

requrl = 'https://api.telegram.org/bot198568784:AAHPV1DGVN9HQagvR8z5r1kSHGd5JxtjS60/'
commands = ['add', 'remove', 'help']


class bot:
    api_token = None
    requestUrl = 'https://api.telegram.org/bot{0}'.format(api_token)
    quotes = None

    def __init__(self, api_key):
        self.api_token = api_key
        self.quotes = {}

    def getUpdates(self):
        r = requests.post(requrl + 'getUpdates').json()
        if not r['ok']:
            return -1
        if r['result'] == []:
            return 0
        update_id = r['result'][len(r['result']) - 1]['update_id']
        requests.post(requrl + 'getUpdates', data={'offset': update_id + 1})
        return r

    def sendMessage(self, chat_id, message_text):
        r = requests.post(requrl + 'sendMessage', data={'chat_id': chat_id, 'text': message_text}).json()
        if not r['ok']:
            return -1
        return r

    def sendReply(self, chat_id, message_text, user_id):
        r = requests.post(requrl + 'sendMessage', data={'chat_id': chat_id, 'text': message_text, 'reply_to_message_id': user_id}).json()
        if not r['ok']:
            return -1
        return r

    def loadQuoteFile(self):
        if not os.path.exists('quotelist.qt'):
            self.quotes = {}
            return
        with open('quotelist.qt', 'rb') as filedescriptor:
            self.quotes = pickle.load(filedescriptor)

def main():
    quotebot = bot('198568784:AAHPV1DGVN9HQagvR8z5r1kSHGd5JxtjS60')
    quotebot.loadQuoteFile()
    while 1:
        request = quotebot.getUpdates()
        if request == 0:
            continue
        else:
            chat_id = request['result'][len(request['result'])-1]['message']['chat']['id']
            msg = request['result'][len(request['result'])-1]['message']['text']
            response = botcommand.parse(quotebot, msg)
            quotebot.sendMessage(chat_id, response)
            continue


if __name__ == '__main__':
    main()
