import asyncio
import html

import websockets
from slack_sdk import WebClient


async def chat_handler(websocket, path):
    name = await websocket.recv()
    global clients
    clients.add(websocket)

    text = '{} joined the conversation'.format(name)
    slack_client.chat_postMessage(channel='#chat-bot', text=text)

    for client in clients:
        await client.send(text)

    while True:
        try:
            message = await websocket.recv()
            message = html.escape(message)
            text = '<b>{}:</b> {}'.format(name, message)
            print('{}: {}'.format(name, message))
            slack_client.chat_postMessage(channel='#chat-bot', text=text)
            for client in clients:
                await client.send(text)
        except:
            clients.remove(websocket)
            text = '{} left the conversation'.format(name)
            print(text)
            slack_client.chat_postMessage(channel='#chat-bot', text=text)

            for client in clients:
                await client.send(text)


if __name__ == '__main__':
    clients = set()

    slack_client = WebClient(token='xoxb-1956992088320-1991654770804-gFsXZQsAjLpMHztvjARtsacy')

    start_server = websockets.serve(chat_handler, 'localhost', 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
