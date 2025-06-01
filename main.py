from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Events import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
import requests
import os

class ChatGPTExtension(Extension):
    def __init__(self):
        super(ChatGPTExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or ''
        results = []

        if not query.strip():
            results.append(ExtensionResultItem(
                icon='images/icon.png',
                name='Skriv et spørgsmål efter "c "',
                description='Eksempel: c Hvad er vejret i København?',
                on_enter=None
            ))
            return RenderResultListAction(results)

        # Læs API-nøgle fra lokal fil
        api_key_path = os.path.expanduser('~/.config/chatgpt_api_key.txt')
        if not os.path.isfile(api_key_path):
            results.append(ExtensionResultItem(
                icon='images/icon.png',
                name='API-nøgle ikke fundet',
                description=f'Gem din OpenAI API-nøgle i {api_key_path}',
                on_enter=None
            ))
            return RenderResultListAction(results)

        with open(api_key_path, 'r') as f:
            api_key = f.read().strip()

        # OpenAI API kald
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }
        json_data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": query}],
            "max_tokens": 150,
            "temperature": 0.7
        }

        try:
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data)
            response.raise_for_status()
            data = response.json()
            answer = data['choices'][0]['message']['content'].strip()
        except Exception as e:
            answer = f"Fejl ved API kald: {e}"

        results.append(ExtensionResultItem(
            icon='images/icon.png',
            name=answer,
            description='Svar fra ChatGPT',
            on_enter=None
        ))

        return RenderResultListAction(results)

if __name__ == '__main__':
    ChatGPTExtension().run()
