from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
<head>
    <title>예쁜 채팅방</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #e5ddd5;
            display: flex;
            flex-direction: column;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        #chat_container {
            background-color: #ffffff;
            width: 400px;
            height: 500px;
            margin-top: 20px;
            padding: 10px;
            overflow-y: scroll;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .message {
            margin: 10px 0;
            padding: 8px 12px;
            border-radius: 10px;
            max-width: 70%;
            word-wrap: break-word;
        }
        .me {
            background-color: #dcf8c6;
            margin-left: auto;
            text-align: right;
        }
        .other {
            background-color: #ffffff;
            margin-right: auto;
            text-align: left;
            border: 1px solid #ccc;
        }
        #input_area {
            width: 400px;
            margin-top: 10px;
            display: flex;
        }
        #message_input {
            flex: 1;
            padding: 10px;
            border: none;
            border-radius: 5px;
        }
        #send_button {
            padding: 10px 20px;
            border: none;
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            margin-left: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h2>카톡 스타일 채팅방</h2>
    <div id="chat_container"></div>

    <div id="input_area">
        <input id="message_input" type="text" placeholder="메시지 입력...">
        <button id="send_button" onclick="sendMessage()">보내기</button>
    </div>

    <script>
        var ws = new WebSocket("ws://localhost:8080/ws");
        var nickname = prompt("닉네임을 입력하세요:");
        
        ws.onmessage = function(event) {
            var chatContainer = document.getElementById('chat_container');
            var messageBox = document.createElement('div');
            const [sender, ...msgArr] = event.data.split(": ");
            const message = msgArr.join(": ");

            if (sender === nickname) {
                messageBox.className = 'message me';
            } else {
                messageBox.className = 'message other';
            }
            messageBox.textContent = event.data;
            chatContainer.appendChild(messageBox);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        };

        function sendMessage() {
            var input = document.getElementById("message_input");
            var message = nickname + ": " + input.value;
            ws.send(message);
            input.value = '';
        }
    </script>
</body>
</html>
"""

connections = []

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # 모두에게 메시지 보내기
            for conn in connections:
                await conn.send_text(data)
    except WebSocketDisconnect:
        connections.remove(websocket)
