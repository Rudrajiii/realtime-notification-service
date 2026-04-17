// const ws = new WebSocket("ws://localhost:8000/ws/1");

// ws.onopen = () => {
//     console.log("user_id 1 connected to server...");
// }

// ws.onmessage = (event) => {
//     console.log("Notification: " , event.data);
// }

// ws.onclose = () => {
//     console.log("Disconnected");
// };

function connectTenUsers(){
    for(let user_id = 1 ; user_id < 11 ; user_id++){
        const ws = new WebSocket(`ws://localhost:8000/ws/${user_id}`);
        ws.onopen = () => {
            console.log(`user_id ${user_id} connected to server...`);
        }

        ws.onmessage = (event) => {
            console.log("Notification: " , event.data);
        }

        ws.onclose = () => {
            console.log("Disconnected");
        };
    }
}



connectTenUsers()