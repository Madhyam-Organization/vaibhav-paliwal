const room_id = JSON.parse(document.getElementById('room_id').textContent)
const logged_in_user = JSON.parse(document.getElementById('logged_in_user').textContent)

// Create a new WebSocket
const chatSocket = new WebSocket('ws://'+ window.location.host +'/ws/direct/' + room_id + "/");


document.getElementById('send-button').onclick = function(e){
    e.preventDefault();
    const messageInput = document.getElementById('message-input');
    const chat_message = messageInput.value;

    messageInput.value = ""
    chatSocket.send(JSON.stringify({
        'message_sender': logged_in_user,
        'message_content': chat_message
    }))
}

// Application layer Headers dont work on HTTP
chatSocket.onmessage = function(e){
    data = JSON.parse(e.data)
    let message_content = data.message_content
    let message_sender = data.message_sender
    let html = `<tr>
                    <td>
                        <p class="bg-success float-right chat_message p-2 mt-2 mr-5 shadow-sm text-white rounded ">
                            ${message_content}
                            <small class="ml-2" style="font-size: 12px; color:#8FBEA6;">just now</small>
                        </p>
                    </td>
                </tr> `
    let newhtml =` <tr>
                    <td>
                        <p class="bg-primary float-left chat_message p-2 mt-2 mr-5 shadow-sm text-white rounded ">
                            ${message_content}
                            <small class="ml-2" style="font-size: 12px; color:#8FBEA6;">just now</small>
                        </p>
                    </td>
                </tr>`

    if(logged_in_user == message_sender)
        document.getElementById('displayed_messages').insertAdjacentHTML('beforeend', html)
    else
        document.getElementById('displayed_messages').insertAdjacentHTML('beforeend', newhtml)

    //scroll();       // whenever we get a new message we will scroll to top
}


/*function scroll(){
    const mcontainer = document.getElementById('chat-container');
    mcontainer.scrollTop = mcontainer.scrollHeight;
}

scroll()*/




//javascript object->json object
//JSON.stringify()
//json object->javascript object
//JSON.parse()

//python object->json obj
//json.dumps()
//json obj->python obj
//json.loads()
