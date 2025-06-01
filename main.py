import os
import requests
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Events import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction

# Filsti til din API-nøgle (ret hvis du vil have den et andet sted)
API_KEY_PATH = os.path.expanduser("~/.config/chatgpt_api_key")

class ChatGPTExtension(Extension):

    def __init__(self):
        super(ChatGPTExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        query = event.get_argument() or ""

        results = []

        if not query.strip():
            results.append(
                ExtensionResultItem(
                    icon="images/icon.png",
                    name='Skriv et spørgsmål efter "c "',
                    description="Eksempel: c hvad er vejret i København?",
                    on_enter=None,
                )
            )
            return RenderResultListAction(results)

        # Læs API-nøglen
        try:
            with open(API_KEY_PATH, "r") as f:
                api_key = f.read().strip()
        except Exception as e:
            results.append(
                ExtensionResultItem(
                    icon="images/icon.png",
                    name="Fejl: Kunne ikke læse API-nøgle",
                    description=str(e),
                    on_enter=None,
                )
            )
            return RenderResultListAction(results)

        # OpenAI API kald (Chat Completion v1)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": query}],
            "max_tokens": 200,
            "temperature": 0.7,
        }

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions", json=data, headers=headers
            )
            response.raise_for_status()
            result_json = response.json()
            answer = result_json["choices"][0]["message"]["content"].strip()
        except Exception as e:
            results.append(
                ExtensionResultItem(
                    icon="images/icon.png",
                    name="Fejl ved API kald",
                    description=str(e),
                    on_enter=None,
                )
            )
            return RenderResultListAction(results)

        results.append(
            ExtensionResultItem(
                icon="images/icon.png",
                name=answer,
                description="Svar fra ChatGPT",
                on_enter=None,
            )
        )

        return RenderResultListAction(results)


if __name__ == "__main__":
    ChatGPTExtension().run()
