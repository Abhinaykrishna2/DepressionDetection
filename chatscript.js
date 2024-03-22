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
    if(response.nextEvent=='finish')
    {
        document.getElementById('end-display').innerText= 'PCAB chatbot is only a primary testing tool, might produce inaccurate information some times.'
        socket.close();
        if (response.nextEvent === 'finish') {
            window.location.href = 'new_page.html?message=' + encodeURIComponent(response.opt);
        }
    }
    else if(response.nextEvent=='finish')
    {
        document.getElementById('end-display').innerText= 'Thank you for using PCAB, please note that PCAB may produce wrong information';
        document.getElementById('chat-body').innerText=response.ans;
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
