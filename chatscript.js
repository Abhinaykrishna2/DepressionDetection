const socket = new WebSocket('ws://localhost:5000'); // Connect to the WebSocket server

socket.addEventListener('message', function (event) {
    const chatMessages = document.getElementById('chat-messages');
    const message = document.createElement('div');
    message.className = 'message bot';
    message.innerHTML = '<p>' + event.data + '</p>';
    chatMessages.appendChild(message);
    chatMessages.scrollTop = chatMessages.scrollHeight;
});

function sendMessage() {
    const answerInput = document.getElementById('answerInput');
    const answer = answerInput.value;

    const chatMessages = document.getElementById('chat-messages');
    const message = document.createElement('div');
    message.className = 'message user';
    message.innerHTML = '<p>' + answer + '</p>';
    chatMessages.appendChild(message);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    socket.send(answer);
    answerInput.value = '';
}
