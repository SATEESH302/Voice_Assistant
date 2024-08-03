from fastapi import FastAPI, WebSocket, WebSocketDisconnect , Request
from fastapi.responses import FileResponse

import openai
import time
import os
from speech_to_text import get_answer_for_question
from constants import open_ai_key

app = FastAPI()

response = ""

os.environ["OPENAI_API_KEY"] =  open_ai_key #OPENAI_API_KEY

client = openai.OpenAI()

# record the time before the request is sent
start_time = time.time()


def call_open_api(message):
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        
        messages=[
            {"role": "system", "content": "You are a assistance named Bluu , A asistance from scalebuildAI , you help people to find the best product for them , Scalebuild ios a software company"},
            #add 10 last messages history here

            {'role': 'user', 'content': message}
        ],
        temperature=0,
        stream=True  # again, we set stream=True
    )

    return completion
    # create variables to collect the stream of chunks
    
    
    

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
    try:
        while True:
            try:
                # Receive text data (speech recognition result) from the client
                data = await websocket.receive_text()
                
                # Process the data
                print(f"Received text: {data}")  # Example: print it to the console
                res = get_answer_for_question(data)

                # response = "Question: " + data + response + "\n"

                if len(res) > 0:
                    message = [m for m in res if m is not None]
                    full_reply_content = ''.join([m for m in message])

                    response =   "Question: " + data + "\n" + "Answer: "  +full_reply_content + ";\n\n" + response

                    res_list = response.split(";")
                    print("Question: " + data)
                    print("Answer: "  +full_reply_content)

                    response = ";\n".join(res_list)

                    await manager.send_text(response, websocket)
                    res = []
                
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