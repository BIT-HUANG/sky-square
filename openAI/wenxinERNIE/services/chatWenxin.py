from portalUtils.Logger import Logger
from openAI.wenxinERNIE.utils.server import ErnieServ

chat_history = list()


class ChatWenxin:
    def __init__(self):
        self.ernie_logger = Logger.get_logger("SKY", "ChatWenxin")
        self.ES = ErnieServ()

    def talk_to_bot(self, ask):
        ES = ErnieServ()
        msg = self.asm_chat_history(ask)
        global chat_history
        chat_history = ES.send_msg(msg)
        self.ernie_logger.info('get bot answer. now history is: ')
        self.ernie_logger.info(chat_history)
        return chat_history

    @staticmethod
    def asm_chat_history(content):
        chat_history.append({"role": "user", "content": content})
        return chat_history

    def clean_chat_history(self):
        global chat_history
        chat_history = []
        self.ernie_logger.info('clean chat history. now history is: ')
        self.ernie_logger.info(chat_history)
        return chat_history


