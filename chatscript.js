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

function sendMessage() {
    const socket = new WebSocket("ws://localhost:8005/");
    var intopt = document.getElementById('ipms').value;  // Assuming 'ipms' is an input element

    // Wait for the WebSocket to open before sending the message
    socket.addEventListener('open', function (event) {
        // Send the intopt value to the Python server
        socket.send(JSON.stringify({ intopt: intopt }));
    });
}
