import requests

class HTTP:
    API_URL = 'https://discord.com/api/v9'

    def __init__(self, token):
        self.token = token

    def send_message(self, channel_id:int, message:str):
        url = self.API_URL + f'/channels/{channel_id}/messages'
        print(url)
        headers = {
            'Authorization': f'Bot your_authorization_token'
        }
        payload = {
            'content': message
        }
        response = requests.post(url, headers=headers, json=payload).json()
        print(response)