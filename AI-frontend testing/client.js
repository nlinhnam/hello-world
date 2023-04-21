
document.addEventListener('DOMContentLoaded', function(){
    const client = new WebSocket("ws://localhost:8000/");

    const messageInput = document.querySelector("[name=message_input]");
    const sendMessage = document.querySelector("[name=message_button_input]");
    const messageOutput = document.querySelector("[name=message_output]");

    client.onopen = function(){
        console.log("Client Connected");

        sendMessage.onclick = function(){
            client.send(messageInput.value);
        };

        client.onmessage = function(e){
            console.log("Recv: " + e.data);
            messageOutput.value = e.data;
        };
    };

}, false)