import webview
from threading import Thread, Event
import uvicorn
from app import app  # Assuming app.py is your FastAPI application
from webview.dom import DOMEventHandler

def on_drag(e):
    pass

def on_drop(e):
    files = e['dataTransfer']['files']
    if len(files) == 0:
        return

    print(f'Event: {e["type"]}. Dropped files:')

    for file in files:
        print(file.get('pywebviewFullPath'))

def bind(window):
    window.dom.document.events.dragenter += DOMEventHandler(on_drag, True, True)
    window.dom.document.events.dragstart += DOMEventHandler(on_drag, True, True)
    window.dom.document.events.dragover += DOMEventHandler(on_drag, True, True, debounce=500)
    window.dom.document.events.drop += DOMEventHandler(on_drop, True, True)
    
# This event will be set when we need to stop the FastAPI server
stop_event = Event()

app_title = "Package Info Validator App"
host = "127.0.0.1"
port = 8001
#custom_path = "35485"  # The desired URL path

def run():
    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)
    
    # Run the server until the stop event is set
    while not stop_event.is_set():
        server.run()

    # Gracefully shut down the server
    server.should_exit = True

class Api:

  def __init__(self):
    self._window = None

  def set_window(self, window):
    self._window = window

  def quit(self):
    self._window.destroy()
    
api = Api()    
    
if __name__ == '__main__':     
    t = Thread(target=run)
    t.daemon = True  # Ensures the thread exits when the main program exits
    t.start()

    # Create the webview window with the custom path
    window = webview.create_window(
        app_title,
        f"http://{host}:{port}/",
        resizable=True,
        height=450,
        width=1100,
        frameless=False,
        easy_drag=True,
        on_top=False,
        draggable=True,
        js_api=api
    ) 
    api.set_window(window)
    webview.start()

    # webview.start(bind, window)

    # Signal FastAPI server to shut down
    stop_event.set()

#pyinstaller -F run.py
#uv run pyinstaller run.spec