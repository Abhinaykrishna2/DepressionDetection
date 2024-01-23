import asyncio
import websockets
import json

async def handle_message(websocket, path):
    async for message in websocket:
        # Parse the JSON message
        data = json.loads(message)

        # Access the 'intopt' value
        intopt_value = data.get('intopt', '')

        # Process the intopt_value as needed
        # ...

        # Send a response if necessary
        response = {'status': 'success'}
        await websocket.send(json.dumps(response))

start_server = websockets.serve(handle_message, "localhost", 8005)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
