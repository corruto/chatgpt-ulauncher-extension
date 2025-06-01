import os
from pathlib import Path
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Events import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
import requests
import json

class ChatGPTExtension(Extension):
    def __init__(self):
        super(ChatGPTExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.api_key = self.load_api_key()

    def load_api_key(self):
        config_path = Path.home() / ".config" / "chatgpt_ulauncher" / "api_key.txt"
        if config_path.exists():
            return config_path.read_text().strip()
        else:
            self.logger.error(f"API key file not found: {config_path}")
            return None

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or ''
        results = []

        if not extension.api_key:
            results.append(ExtensionResultItem(
                icon='images/icon.png',
                name='API-nøgle ikke fundet',
                description='Gem din OpenAI API-nøgle i ~/.config/chatgpt_ulauncher/api_key.txt',
                on_enter=None
            ))
            return RenderResultListAction(results)

        if not query.strip():
            results.append(ExtensionResultItem(
                icon='images/icon.png',
                name='Skriv et spørgsmål efter "c "',
                description='Eksempel: c hvad er vejret i København?',
                on_enter=None
            ))
            return RenderResultListAction(results)

        # Kald OpenAI Chat Completion API
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {extension.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": query}],
                    "max_tokens": 200,
                    "temperature": 0.7,
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            answer = data['choices'][0]['message']['content'].strip()

        except Exception as e:
            answer = f"Fejl ved API-kald: {e}"

        results.append(ExtensionResultItem(
            icon='images/icon.png',
            name=answer,
            description='Svar fra ChatGPT',
            on_enter=None
        ))
        return RenderResultListAction(results)

if __name__ == '__main__':
    ChatGPTExtension().run()
