import asyncio
import json
import websockets
import time
import openai
import numpy as np
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D

openai.api_key = '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'

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
            "msg" : "Please enter your current problems",
            "option" : [],
            "nextEvent" : 'LLMcall',
        }
        await send_response(response, websocket)
        user_response = await asyncio.wait_for(websocket.recv(), timeout=100)
        print('++++++++++++++',user_response)
        temp=user_response.split('==')
        print("{}('{}', websocket)".format(temp[1], user_response))
        await eval("{}('{}', websocket)".format(temp[1], user_response))
    elif re[0].lower() == 'depression test':
        camcall()
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
        user_response = await asyncio.wait_for(websocket.recv(), timeout=100)
        print('++++++++++++++',user_response)
        temp=user_response.split('==')
        print("{}('{}', websocket)".format(temp[1], user_response))
        await eval("{}('{}', websocket)".format(temp[1], user_response))
    else:
        await default_response(websocket)
    
async def LLMcall(data,websocket):
    print(data)
    req=data.split('==')
    question = '{}, strictly suggest me with appropriate medicine or recovery procedure, the response has to be in a proper format with no more than 150 tokens'.format(req[0])
    prompt = f"Question: {question}\nAnswer:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[{"role": "system", "content": prompt}],
    )
    answer = response['choices'][0]['message']['content']
    response={
        'ans' : answer,
        'nextEvent' : 'endMed'
    }
    print(answer)
    print('+++++++++LLM Response Generated')
    await send_response(response, websocket)



async def q1(data, websocket):
    print(data)
    pcab=data.split('==')
    req=pcab[0].split('-')
    print(int(req[0]))
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
    camcall()
    await send_response(response, websocket)
    user_response = await asyncio.wait_for(websocket.recv(), timeout=100)
    print('++++++++++++++',user_response)
    temp=user_response.split('==')
    print("{}('{}', websocket)".format(temp[1], user_response))
    await eval("{}('{}', websocket)".format(temp[1], user_response))

async def q2(data, websocket):
    print(data)
    pcab=data.split('==')
    req=pcab[0].split('-')
    print(int(req[0]))
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
    user_response = await asyncio.wait_for(websocket.recv(), timeout=100)
    print('++++++++++++++',user_response)
    temp=user_response.split('==')
    print("{}('{}', websocket)".format(temp[1], user_response))
    await eval("{}('{}', websocket)".format(temp[1], user_response))

async def q3(data, websocket):
    print(data)
    pcab=data.split('==')
    req=pcab[0].split('-')
    print(int(req[0]))
    response={
            "msg" : "I experienced breathing difficulty (e.g. excessively rapid breathing, breathlessness in the absence of physical exertion) ",
            "option" : ["1- Did not apply to me at all",
                        "2- Applied to me to some degree, or some of the time",
                        "3- Applied to me to a considerable degree or a good part of time",
                        "4- Applied to me very much or most of the time"],
            "nextEvent" : 'q4',
            "cnt" : int(req[0])
        }
    print('=====================','Reached here q3')
    await send_response(response, websocket)
    user_response = await asyncio.wait_for(websocket.recv(), timeout=100)
    print('++++++++++++++',user_response)
    temp=user_response.split('==')
    print("{}('{}', websocket)".format(temp[1], user_response))
    await eval("{}('{}', websocket)".format(temp[1], user_response))

async def q4(data, websocket):
    print(data)
    pcab=data.split('==')
    req=pcab[0].split('-')
    camcall()
    print(int(req[0]))
    response={
            "msg" : "I found it difficult to work up the initiative to do things",
            "option" : ["1- Did not apply to me at all",
                        "2- Applied to me to some degree, or some of the time",
                        "3- Applied to me to a considerable degree or a good part of time",
                        "4- Applied to me very much or most of the time"],
            "nextEvent" : 'q5',
            "cnt" : int(req[0])
        }
    print('=====================','Reached here')
    await send_response(response, websocket)
    user_response = await asyncio.wait_for(websocket.recv(), timeout=100)
    print('++++++++++++++',user_response)
    temp=user_response.split('==')
    print("{}('{}', websocket)".format(temp[1], user_response))
    await eval("{}('{}', websocket)".format(temp[1], user_response))

async def q5(data, websocket):
    print(data)
    pcab=data.split('==')
    req=pcab[0].split('-')
    
    response={
            "msg" : "I tended to over-react to situations",
            "option" : ["1- Did not apply to me at all",
                        "2- Applied to me to some degree, or some of the time",
                        "3- Applied to me to a considerable degree or a good part of time",
                        "4- Applied to me very much or most of the time"],
            "nextEvent" : 'q6',
            "cnt" : int(req[0])
        }
    print('=====================','Reached here q5')
    await send_response(response, websocket)
    user_response = await asyncio.wait_for(websocket.recv(), timeout=100)
    print('++++++++++++++',user_response)
    temp=user_response.split('==')
    print("{}('{}', websocket)".format(temp[1], user_response))
    await eval("{}('{}', websocket)".format(temp[1], user_response))

async def q6(data, websocket):
    print(data)
    pcab=data.split('==')
    req=pcab[0].split('-')
    print(int(req[0]))
    response={
            "msg" : "I experienced trembling (e.g. in the hands)",
            "option" : ["1- Did not apply to me at all",
                        "2- Applied to me to some degree, or some of the time",
                        "3- Applied to me to a considerable degree or a good part of time",
                        "4- Applied to me very much or most of the time"],
            "nextEvent" : 'q7',
            "cnt" : int(req[0])
        }
    print('=====================','Reached here q6')
    await send_response(response, websocket)
    user_response = await asyncio.wait_for(websocket.recv(), timeout=100)
    print('++++++++++++++',user_response)
    temp=user_response.split('==')
    print("{}('{}', websocket)".format(temp[1], user_response))
    await eval("{}('{}', websocket)".format(temp[1], user_response))

async def q7(data, websocket):
    print(data)
    pcab=data.split('==')
    req=pcab[0].split('-')
    
    response={
            "msg" : "I felt that I was using a lot of nervous energy",
            "option" : ["1- Did not apply to me at all",
                        "2- Applied to me to some degree, or some of the time",
                        "3- Applied to me to a considerable degree or a good part of time",
                        "4- Applied to me very much or most of the time"],
            "nextEvent" : 'q8',
            "cnt" : int(req[0])
        }
    print('=====================','Reached here q7')
    await send_response(response, websocket)
    user_response = await asyncio.wait_for(websocket.recv(), timeout=100)
    print('++++++++++++++',user_response)
    temp=user_response.split('==')
    print("{}('{}', websocket)".format(temp[1], user_response))
    await eval("{}('{}', websocket)".format(temp[1], user_response))

async def q8(data, websocket):
    print(data)
    pcab=data.split('==')
    camcall()
    req=pcab[0].split('-')
    print(int(req[0]))
    response={
            "msg" : "I was worried about situations in which I might panic and make a fool of myself",
            "option" : ["1- Did not apply to me at all",
                        "2- Applied to me to some degree, or some of the time",
                        "3- Applied to me to a considerable degree or a good part of time",
                        "4- Applied to me very much or most of the time"],
            "nextEvent" : 'q9',
            "cnt" : int(req[0])
        }
    print('=====================','Reached here q8')
    await send_response(response, websocket)
    user_response = await asyncio.wait_for(websocket.recv(), timeout=100)
    print('++++++++++++++',user_response)
    temp=user_response.split('==')
    print("{}('{}', websocket)".format(temp[1], user_response))
    await eval("{}('{}', websocket)".format(temp[1], user_response))

async def q9(data, websocket):
    print(data)
    pcab=data.split('==')
    req=pcab[0].split('-')
    
    response={
            "msg" : " I felt that I had nothing to look forward to",
            "option" : ["1- Did not apply to me at all",
                        "2- Applied to me to some degree, or some of the time",
                        "3- Applied to me to a considerable degree or a good part of time",
                        "4- Applied to me very much or most of the time"],
            "nextEvent" : 'q10',
            "cnt" : int(req[0])
        }
    print('=====================','Reached here q9')
    await send_response(response, websocket)
    user_response = await asyncio.wait_for(websocket.recv(), timeout=100)
    print('++++++++++++++',user_response)
    temp=user_response.split('==')
    print("{}('{}', websocket)".format(temp[1], user_response))
    await eval("{}('{}', websocket)".format(temp[1], user_response))

async def q10(data, websocket):
    print(data)
    pcab=data.split('==')
    req=pcab[0].split('-')
    print(int(req[0]))
    response={
            "msg" : "I found myself getting troubled",
            "option" : ["1- Did not apply to me at all",
                        "2- Applied to me to some degree, or some of the time",
                        "3- Applied to me to a considerable degree or a good part of time",
                        "4- Applied to me very much or most of the time"],
            "nextEvent" : 'q11',
            "cnt" : int(req[0])
        }
    print('=====================','Reached here q11')
    await send_response(response, websocket)
    user_response = await asyncio.wait_for(websocket.recv(), timeout=100)
    print('++++++++++++++',user_response)
    temp=user_response.split('==')
    print("{}('{}', websocket)".format(temp[1], user_response))
    await eval("{}('{}', websocket)".format(temp[1], user_response))

async def q11(data, websocket):
    print(data)
    pcab=data.split('==')
    req=pcab[0].split('-')
    
    response={
            "msg" : "I found it difficult to relax",
            "option" : ["1- Did not apply to me at all",
                        "2- Applied to me to some degree, or some of the time",
                        "3- Applied to me to a considerable degree or a good part of time",
                        "4- Applied to me very much or most of the time"],
            "nextEvent" : 'q12',
            "cnt" : int(req[0])
        }
    print('=====================','Reached here q12')
    await send_response(response, websocket)
    user_response = await asyncio.wait_for(websocket.recv(), timeout=100)
    print('++++++++++++++',user_response)
    temp=user_response.split('==')
    print("{}('{}', websocket)".format(temp[1], user_response))
    await eval("{}('{}', websocket)".format(temp[1], user_response))

async def q12(data, websocket):
    print(data)
    pcab=data.split('==')
    req=pcab[0].split('-')
    print(int(req[0]))
    response={
            "msg" : "I felt down-hearted and unhappy",
            "option" : ["1- Did not apply to me at all",
                        "2- Applied to me to some degree, or some of the time",
                        "3- Applied to me to a considerable degree or a good part of time",
                        "4- Applied to me very much or most of the time"],
            "nextEvent" : 'q13',
            "cnt" : int(req[0])
        }
    print('=====================','Reached here q12')
    await send_response(response, websocket)
    user_response = await asyncio.wait_for(websocket.recv(), timeout=100)
    print('++++++++++++++',user_response)
    temp=user_response.split('==')
    print("{}('{}', websocket)".format(temp[1], user_response))
    await eval("{}('{}', websocket)".format(temp[1], user_response))

async def q13(data, websocket):
    print(data)
    pcab=data.split('==')
    camcall()
    req=pcab[0].split('-')
    print(int(req[0]))
    response={
            "msg" : "I was intolerant of anything that kept me from getting on with what I was doing",
            "option" : ["1- Did not apply to me at all",
                        "2- Applied to me to some degree, or some of the time",
                        "3- Applied to me to a considerable degree or a good part of time",
                        "4- Applied to me very much or most of the time"],
            "nextEvent" : 'q14',
            "cnt" : int(req[0])
        }
    print('=====================','Reached here q13')
    await send_response(response, websocket)
    user_response = await asyncio.wait_for(websocket.recv(), timeout=100)
    print('++++++++++++++',user_response)
    temp=user_response.split('==')
    print("{}('{}', websocket)".format(temp[1], user_response))
    await eval("{}('{}', websocket)".format(temp[1], user_response))

async def q14(data, websocket):
    print(data)
    pcab=data.split('==')
    req=pcab[0].split('-')
    print(int(req[0]))  
    response={
            "msg" : "I felt I was close to panic",
            "option" : ["1- Did not apply to me at all",
                        "2- Applied to me to some degree, or some of the time",
                        "3- Applied to me to a considerable degree or a good part of time",
                        "4- Applied to me very much or most of the time"],
            "nextEvent" : 'q15',
            "cnt" : int(req[0])
        }
    print('=====================','Reached here q14')
    await send_response(response, websocket)
    user_response = await asyncio.wait_for(websocket.recv(), timeout=100)
    print('++++++++++++++',user_response)
    temp=user_response.split('==')
    print("{}('{}', websocket)".format(temp[1], user_response))
    await eval("{}('{}', websocket)".format(temp[1], user_response))

async def q15(data, websocket):
    print(data)
    pcab=data.split('==')
    req=pcab[0].split('-')
    camcall()
    print(int(req[0]))  
    response={
            "msg" : "I was unable to become enthusiastic about anything",
            "option" : ["1- Did not apply to me at all",
                        "2- Applied to me to some degree, or some of the time",
                        "3- Applied to me to a considerable degree or a good part of time",
                        "4- Applied to me very much or most of the time"],
            "nextEvent" : 'q16',
            "cnt" : int(req[0])
        }
    print('=====================','Reached here q15')
    await send_response(response, websocket)
    user_response = await asyncio.wait_for(websocket.recv(), timeout=100)
    print('++++++++++++++',user_response)
    temp=user_response.split('==')
    print("{}('{}', websocket)".format(temp[1], user_response))
    await eval("{}('{}', websocket)".format(temp[1], user_response))

async def q16(data, websocket):
    print(data)
    pcab=data.split('==')
    req=pcab[0].split('-')
    print(int(req[0]))  
    response={
            "msg" : "I felt I wasn’t worth much as a person",
            "option" : ["1- Did not apply to me at all",
                        "2- Applied to me to some degree, or some of the time",
                        "3- Applied to me to a considerable degree or a good part of time",
                        "4- Applied to me very much or most of the time"],
            "nextEvent" : 'q17',
            "cnt" : int(req[0])
        }
    print('=====================','Reached here q16')
    await send_response(response, websocket)
    user_response = await asyncio.wait_for(websocket.recv(), timeout=100)
    print('++++++++++++++',user_response)
    temp=user_response.split('==')
    print("{}('{}', websocket)".format(temp[1], user_response))
    await eval("{}('{}', websocket)".format(temp[1], user_response))

async def q17(data, websocket):
    print(data)
    pcab=data.split('==')
    req=pcab[0].split('-')
    print(int(req[0]))  
    response={
            "msg" : "I thought I was quite sensitive",
            "option" : ["1- Did not apply to me at all",
                        "2- Applied to me to some degree, or some of the time",
                        "3- Applied to me to a considerable degree or a good part of time",
                        "4- Applied to me very much or most of the time"],
            "nextEvent" : 'q18',
            "cnt" : int(req[0])
        }
    print('=====================','Reached here q17')
    await send_response(response, websocket)
    user_response = await asyncio.wait_for(websocket.recv(), timeout=100)
    print('++++++++++++++',user_response)
    temp=user_response.split('==')
    print("{}('{}', websocket)".format(temp[1], user_response))
    await eval("{}('{}', websocket)".format(temp[1], user_response))

async def q18(data, websocket):
    print(data)
    pcab=data.split('==')
    req=pcab[0].split('-')
    
    response={
            "msg" : "I was aware of the action of my heart in the absence of physical exertion (e.g. sense of heart rate increase, heart missing a beat)",
            "option" : ["1- Did not apply to me at all",
                        "2- Applied to me to some degree, or some of the time",
                        "3- Applied to me to a considerable degree or a good part of time",
                        "4- Applied to me very much or most of the time"],
            "nextEvent" : 'q19',
            "cnt" : int(req[0])
        }
    print('=====================','Reached here q18')
    await send_response(response, websocket)
    user_response = await asyncio.wait_for(websocket.recv(), timeout=100)
    print('++++++++++++++',user_response)
    temp=user_response.split('==')
    print("{}('{}', websocket)".format(temp[1], user_response))
    await eval("{}('{}', websocket)".format(temp[1], user_response))

async def q19(data, websocket):
    print(data)
    pcab=data.split('==')
    req=pcab[0].split('-')
    
    response={
            "msg" : "I felt scared without any good reason",
            "option" : ["1- Did not apply to me at all",
                        "2- Applied to me to some degree, or some of the time",
                        "3- Applied to me to a considerable degree or a good part of time",
                        "4- Applied to me very much or most of the time"],
            "nextEvent" : 'q20',
            "cnt" : int(req[0])
        }
    print('=====================','Reached here q19')
    await send_response(response, websocket)
    user_response = await asyncio.wait_for(websocket.recv(), timeout=100)
    print('++++++++++++++',user_response)
    temp=user_response.split('==')
    print("{}('{}', websocket)".format(temp[1], user_response))
    await eval("{}('{}', websocket)".format(temp[1], user_response))

async def q20(data, websocket):
    print(data)
    pcab=data.split('==')
    req=pcab[0].split('-')
    
    response={
            "msg" : "I felt that life was meaningless ",
            "option" : ["1- Did not apply to me at all",
                        "2- Applied to me to some degree, or some of the time",
                        "3- Applied to me to a considerable degree or a good part of time",
                        "4- Applied to me very much or most of the time"],
            "nextEvent" : 'q21',
            "cnt" : int(req[0])
        }
    print('=====================','Reached here q20')
    await send_response(response, websocket)
    user_response = await asyncio.wait_for(websocket.recv(), timeout=100)
    print('++++++++++++++',user_response)
    temp=user_response.split('==')
    print("{}('{}', websocket)".format(temp[1], user_response))
    await eval("{}('{}', websocket)".format(temp[1], user_response))

async def q21(data, websocket):
    print(data)
    pcab=data.split('==')
    req=pcab[0].split('-')
    
    response={
            "msg" : "I tended to over-react to situations",
            "option" : ["1- Did not apply to me at all",
                        "2- Applied to me to some degree, or some of the time",
                        "3- Applied to me to a considerable degree or a good part of time",
                        "4- Applied to me very much or most of the time"],
            "nextEvent" : 'end',
            "cnt" : int(req[0])
        }
    print('=====================','Reached here q21')
    await send_response(response, websocket)
    user_response = await asyncio.wait_for(websocket.recv(), timeout=100)
    print('++++++++++++++',user_response)
    temp=user_response.split('==')
    print("{}('{}', websocket)".format(temp[1], user_response))
    await eval("{}('{}', websocket)".format(temp[1], user_response))


async def end(data,websocket):
    print(data)
    camcall()
    pcab=data.split('==')
    req=pcab[0].split('-')
    response={
        'nextEvent':'endDep',
        'cnt' : int(req[0])
    }
    print('=====================','Dep Test Finished')
    await send_response(response, websocket)

async def default_response(websocket):
    print('Default response')
    response = {"msg": "I didn't understand that. Please choose a valid option.", "option": []}
    await send_response(response, websocket)

def camcall():
    cap = cv2.VideoCapture(0)

    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(7, activation='softmax'))
    if cap.isOpened() :
        model.load_weights('model.h5')
        start_time = time.time()
        while (time.time() - start_time) < 2.5:
            ret, frame = cap.read()
            if not ret:
                break
            facecasc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = facecasc.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
                prediction = model.predict(cropped_img)
                maxindex = int(np.argmax(prediction))
                temp = ''
                if maxindex == 0 or maxindex == 2 or maxindex == 5:
                    temp = 'Depressed'
                else:
                    temp = 'Normal'
                cv2.putText(frame, temp, (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.imshow('Video', cv2.resize(frame, (1600, 960), interpolation=cv2.INTER_CUBIC))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return

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
