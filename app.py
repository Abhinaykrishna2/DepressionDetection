import asyncio
import websockets

global_data = {
    'InitialRequest': ''
}  # for data preservance

flags = {}  # for data communication to js websocket

async def handle_connection(websocket, path):
    try:
        async for message in websocket:
            print(f"Received message from client: {message}")

            if message.lower() == 'medical prescription':
                global_data['InitialRequest'] = 'medical prescription'
                msg = 'Sure, May I know what are those medical issues troubling you'

                flags = {
                    'msg': msg,
                    'nextEvent': 'prescribeMedicine',  # function with the same name to be called next
                    'option': []
                }
                await websocket.send(str(flags))
    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed")

async def start_server():
    server = await websockets.serve(handle_connection, "localhost", 8005)
    print("Server started on ws://localhost:8005")

    try:
        await server.wait_closed()
    except asyncio.CancelledError:
        pass

async def main():
    await start_server()

if __name__ == "__main__":
    asyncio.run(main())
