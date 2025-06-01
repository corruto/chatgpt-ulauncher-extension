from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
import requests

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
            # Her indsætter du OpenAI API kaldet
            # Eksempel på placeholder svar:
            response_text = f"Du spurgte: {query}"

            results.append(ExtensionResultItem(
                icon='images/icon.png',
                name=response_text,
                description='Svar fra ChatGPT',
                on_enter=None
            ))

        return RenderResultListAction(results)


if __name__ == '__main__':
    ChatGPTExtension().run()
