import requests
import json
from portalUtils.Logger import Logger
from openAI.wenxinERNIE.config import ErnieConfig as EC


class ErnieServ:
    def __init__(self):
        self.ernie_logger = Logger.get_logger("SKY", "ErnieServ")
        self.API_KEY = EC.API_KEY
        self.SEC_KEY = EC.SEC_KEY
        self.TOKEN_URL = EC.TOKEN_URL
        self.LLAMA_URL = EC.LLAMA_213B_URL

    def get_access_token(self):
        url = self.TOKEN_URL
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        params = {
            'grant_type': 'client_credentials',
            'client_id': self.API_KEY,
            'client_secret': self.SEC_KEY
        }
        payload = json.dumps("")
        response = requests.request("POST", url, params=params, headers=headers, data=payload)
        token = response.json().get("access_token")
        self.ernie_logger.info("token is: " + token)
        return token

    def send_msg(self, chat_history):
        url = self.LLAMA_URL
        params = {
            'access_token': self.get_access_token()
        }
        payload = json.dumps({
            "messages": chat_history
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, params=params, headers=headers, data=payload)
        response_text = json.loads(response.text)
        assistant_answer = response_text['result']
        chat_history.append({"role": "assistant", "content": assistant_answer})
        return chat_history



