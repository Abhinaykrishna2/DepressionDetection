const socket = new WebSocket("ws://127.0.0.1:8005");

socket.addEventListener("open", () => {
    console.log("Connected to Python");
});

var cnt=0;

function generateOptionButtons(options) {
    var optionsContainer = document.getElementById('options-container');
    console.log('#####################'+options);

    optionsContainer.innerHTML = '';

    if(options.length !== 0) {
        var messageParagraph = document.createElement('p');
        messageParagraph.textContent = "Choose an option:";
        optionsContainer.appendChild(messageParagraph);

        for (var i = 0; i < options.length; i++) {
            var button = document.createElement('button');
            button.textContent = options[i];
            button.onclick = function() {
                selectOption(this.textContent);
            };
            optionsContainer.appendChild(button);
        }
    }else{

    }
}


function selectOption(optionText) {
    document.getElementById('user-input').value = optionText;
}

var exampleOptions = ['Medical Prescription', 'Depression Test'];
generateOptionButtons(exampleOptions);

socket.addEventListener("message", (event) => {
    console.log('Breakpoint')
    const response = JSON.parse(event.data);
    console.log("Received response from Python:", response);
    updatedUI(response);
});

function pyconnect(data) {
    socket.send(data);
}
var nextEvent = ''
var bool=true;

function sendMessage() {
    var data = document.getElementById('user-input').value;
    console.log(nextEvent);

    var buttonClickPromise = new Promise(function(resolve, reject) {
        document.getElementById('user-input').addEventListener('input', function() {
            resolve();
        });
    });

    if (exampleOptions[0] == 'Medical Prescription') {
        data += '==' + 'process_data'
    } else { 
        buttonClickPromise.then(function() {
            console.log('Button clicked');
            data=document.getElementById('user-input').value;            
        });
        console.log('#####');
        console.log(data);
        console.log(nextEvent);
        console.log('#####');
        data += '==' + nextEvent;
    }

    console.log(data);
    console.log('Data being sent');
    if(bool)
    {
        pyconnect(data);
        bool=false;
    }
    else{
        bool=true;
    }
    
    document.getElementById('user-input').value = '';
}


function updatedUI(response) {
    console.log('+++++++'+'}'+response.cnt);
    console.log('+++++++'+'}'+response.nextEvent);
    if(response.nextEvent=='endMed')
    {
        socket.close();
        document.getElementById('chat-body').innerText='Problem solved! 😊';
        document.getElementById('end-display').innerHTML= "<br><br><br><br><br><br><br><br><br><br><br><br><p>Thank you for using PCAB. Please note, it may provide incorrect information<p>";
        document.getElementById('ipms').innerText=response.ans;
    }
    else if(response.nextEvent=='endDep')
    {
        socket.close();
        document.getElementById('chat-body').innerText='Depression detection test completed!! 😊';
        document.getElementById('end-display').innerHTML= "<br><br><br><br><br><br><br><br><br><br><br><br><p>Thank you for using PCAB. Please note, it may provide incorrect information<p>";
        if(cnt>=34)
        {
            document.getElementById('ipms').innerText = 'You are experiencing extremely severe Depression, Anxiety and Stress, Please consult a doctor immediately';
        }else if(cnt>=20 && cnt<34)
        {
            document.getElementById('ipms').innerText = 'You are experiencing moderate Depression and Stress, extreme Anxiety, Please try to consult a doctor';
        }
        else if(cnt>14 && cnt<20)
        {
            document.getElementById('ipms').innerText = "You are experiencing mild depression, anxiety, and stress. You may plan on visiting a doctor";
        }else{
            document.getElementById('ipms').innerText = "Your indicators are normal, there is no need of visiting a doctor";
        }
        document.getElementById('options-container').innerText = '';
    }
    else{
        console.log('Printing msg :'+response.msg);
        console.log('Printing options : '+response.option)
        document.getElementById('chat-body').innerText = response.msg;
        exampleOptions = response.option;
        generateOptionButtons(exampleOptions);
        document.getElementById('user-input').value = '';
        cnt+=response.cnt -1;
        console.log('--------------'+cnt+response.cnt);
        console.log(cnt);
        console.log('--------------');
        nextEvent=response.nextEvent;
        sendMessage();
    }
}
