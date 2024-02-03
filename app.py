import asyncio
import json
import websockets


async def handle_connection(websocket, path):
    print('Connected to JS')

    while True:
        data = await websocket.recv()
        if not data:
            break  

        re=data.split('==')
        print()
        await process_data(data, websocket)

async def process_data(websocket):
    data = await websocket.recv()
    print(data)
    re=data.split('==')
    if re[0].lower() == 'medical prescription':
        response={
            "msg" : "May I kindly request a brief description of your current medical condition?",
            "option" : [],
        }
        await send_response(response, websocket)
    elif re[0].lower() == 'depression test':
        response={
            "msg" : "I had trouble relaxing and calming down.",
            "option" : ["1- Did not apply to me at all",
                        "2- Applied to me to some degree, or some of the time",
                        "3- Applied to me to a considerable degree or a good part of time",
                        "4- Applied to me very much or most of the time"],
            "nextEvent" : 'q1',
            "cnt" : 0
        }
        await send_response(response, websocket)
        user_response = await asyncio.wait_for(websocket.recv(), timeout=10)
        print('++++++++++++++',user_response)
        temp=user_response.split('==')
        print("{}('{}', websocket)".format(temp[1], user_response))
        await eval("{}('{}', websocket)".format(temp[1], user_response))
    else:
        await default_response(websocket)

async def q1(data, websocket):
    print(data)
    pcab=data.split('==')
    req=pcab[0].split('-')
    response={
            "msg" : "I was aware of dryness of my mouth.",
            "option" : ["1- Did not apply to me at all",
                        "2- Applied to me to some degree, or some of the time",
                        "3- Applied to me to a considerable degree or a good part of time",
                        "4- Applied to me very much or most of the time"],
            "nextEvent" : 'q2',
            "cnt" : int(req[0])

        }
    print('=====================','Reached here')
    await send_response(response, websocket)
    user_response = await asyncio.wait_for(websocket.recv(), timeout=10)
    print('++++++++++++++',user_response)
    temp=user_response.split('==')
    print("{}('{}', websocket)".format(temp[1], user_response))
    await eval("{}('{}', websocket)".format(temp[1], user_response))

async def q2(data, websocket):
    print(data)
    pcab=data.split('==')
    req=pcab[0].split('-')
    response={
            "msg" : "I couldn’t seem to experience any positive feeling at all",
            "option" : ["1- Did not apply to me at all",
                        "2- Applied to me to some degree, or some of the time",
                        "3- Applied to me to a considerable degree or a good part of time",
                        "4- Applied to me very much or most of the time"],
            "nextEvent" : 'q3',
            "cnt" : int(req[0])

        }
    print('=====================','Reached here')
    await send_response(response, websocket)
    user_response = await asyncio.wait_for(websocket.recv(), timeout=10)
    print('++++++++++++++',user_response)
    temp=user_response.split('==')
    print("{}('{}', websocket)".format(temp[1], user_response))
    await eval("{}('{}', websocket)".format(temp[1], user_response))

async def q3(data, websocket):
    print(data)
    pcab=data.split('==')
    req=pcab[0].split('-')
    response={
            "msg" : "I experienced breathing difficulty (e.g. excessively rapid breathing, breathlessness in the absence of physical exertion) ",
            "option" : ["1- Did not apply to me at all",
                        "2- Applied to me to some degree, or some of the time",
                        "3- Applied to me to a considerable degree or a good part of time",
                        "4- Applied to me very much or most of the time"],
            "nextEvent" : 'q2',
            "cnt" : int(req[0])

        }
    print('=====================','Reached here')
    await send_response(response, websocket)
    user_response = await asyncio.wait_for(websocket.recv(), timeout=10)
    print('++++++++++++++',user_response)
    temp=user_response.split('==')
    print("{}('{}', websocket)".format(temp[1], user_response))
    await eval("{}('{}', websocket)".format(temp[1], user_response))





async def default_response(websocket):
    print('Default response')
    response = {"msg": "I didn't understand that. Please choose a valid option.", "option": []}
    await send_response(response, websocket)

async def send_response(response, websocket):
    response_json = json.dumps(response)
    await websocket.send(response_json)

async def main():
    server = await websockets.serve(
        process_data, '0.0.0.0', 8005
    )

    async with server:
        await server.wait_closed()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
