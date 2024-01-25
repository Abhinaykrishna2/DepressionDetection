function generateOptionButtons(options) {
    var optionsContainer = document.getElementById('options-container');
    if(options.length!=0) {
    optionsContainer.innerHTML = "<p>Choose an option:</p>";
    }

    for (var i = 0; i < options.length; i++) {
        var button = document.createElement('button');
        button.textContent = options[i];
        button.onclick = function() {
            selectOption(this.textContent);
        };
        optionsContainer.appendChild(button);
    }
}
function selectOption(optionText) {
    document.getElementById('user-input').value = optionText;
}
var exampleOptions = ['Medical Prescription', 'Depression Test'];
generateOptionButtons(exampleOptions);

const socket = new WebSocket("ws://localhost:8005");

function pyconnect(data){
    
    socket.addEventListener("open", () => {
        console.log("Connected to Python");
        socket.send(data);
    });
    var response;
    socket.addEventListener("message", (event) => {
        response = event.data;
        console.log(`Received message from Python: ${response}`);
    });
    return response;
}

function sendMessage() {
    var data = document.getElementById('user-input').value;
    console.log('Data being sent')
    pyconnect(data)
}
