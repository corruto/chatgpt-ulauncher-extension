import os
import requests
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Events import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction

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
                description='Eksempel: c hvad er vejret i København?',
                on_enter=None
            ))
        else:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                response_text = "Fejl: OPENAI_API_KEY er ikke sat."
            else:
                try:
                    response = requests.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {api_key}",
                            "Content-Type": "application/json",
                        },
                        json={
                            "model": "gpt-4o",
                            "messages": [{"role": "user", "content": query}]
                        }
                    )
                    response_text = response.json()["choices"][0]["message"]["content"]
                except Exception as e:
                    response_text = f"Fejl i API kald: {str(e)}"

            results.append(ExtensionResultItem(
                icon='images/icon.png',
                name=response_text.strip(),
                description='Svar fra ChatGPT',
                on_enter=None
            ))

        return RenderResultListAction(results)

if __name__ == '__main__':
    ChatGPTExtension().run()
