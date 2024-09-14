from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import FileResponse

import openai
import time
import os
from speech_to_text import get_answer_for_question, initialize_messages, messages
from constants import open_ai_key
import json

app = FastAPI()

response = ""
chat_initialization_done = False

os.environ["OPENAI_API_KEY"] = open_ai_key  # OPENAI_API_KEY

client = openai.OpenAI()


class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_text(self, text: str, websocket: WebSocket):
        await websocket.send_text(text)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    global response
    global chat_initialization_done
    global messages
    try:
        while True:
            try:
                # Receive text data (speech recognition result) from the client
                data = await websocket.receive_text()

                # Initialize a list to store questions and answers if not already initialized
                if "qa_list" not in globals():
                    global qa_list
                    qa_list = []

                # Process the data
                print(f"Received text: {data}")  # Example: print it to the console
                data = json.loads(data)

                # Run initialize_messages() only once
                if not chat_initialization_done:
                    initialize_messages(domain=data["domain"], jd=data["jd"])
                    chat_initialization_done = True

                res = get_answer_for_question(data["question"])

                # Append the question to the list
                # qa_list.append(f"{data}")

                if len(res) > 0:
                    message = [m for m in res if m is not None]
                    full_reply_content = "".join([m for m in message])

                    # Append the answer to the list
                    qa_list.append(f'{data["question"]}')
                    qa_list.append(f"{full_reply_content}")

                    # Only keep the latest 6 elements (3 questions and 3 answers)
                    if len(qa_list) > 6:
                        qa_list = qa_list[-6:]

                    print("qa_list", qa_list)
                    response = "$".join(qa_list)
                    await manager.send_text(response, websocket)
            except WebSocketDisconnect:
                manager.disconnect(websocket)
                break
            except Exception as e:
                # Handle other exceptions
                print(f"Error: {str(e)}")
                break
    finally:
        manager.disconnect(websocket)


# api to acces htmlpage call voice.html
@app.get("/")
async def get():
    return FileResponse("voice_frontend.html")


@app.get("/script.js")
async def get_js():
    return FileResponse("script.js")
