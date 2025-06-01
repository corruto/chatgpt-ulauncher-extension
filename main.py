from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction

class TestExtension(Extension):
    def __init__(self):
        super(TestExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or ''
        results = [
            ExtensionResultItem(
                icon='images/icon.png',
                name='Test: ' + query,
                description='Dette er en test',
                on_enter=None
            )
        ]
        return RenderResultListAction(results)

if __name__ == '__main__':
    TestExtension().run()
