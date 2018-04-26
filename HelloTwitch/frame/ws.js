var socket = new WebSocket(API_Socket);

socket.onopen = function() { // Format your Authentication Information
	var auth = {
		author: "AnkhHeart",
		website: "https://github.com/PakL/HelloTwitch",
		api_key: API_Key,
		events: [ "HELLO_TWITCH_GREETING" ]
	}
	// Send your Data to the server
	socket.send(JSON.stringify(auth))
	
	statusOutput.innerText = 'Authenticating...'
}

socket.onerror = function(error) {
	statusOutput.innerText = 'Error: ' + error
	console.error(error)
}
socket.onmessage = function (message) {
	// You have received new data now process it
	var data = JSON.parse(message.data)
	if(data.event == 'HELLO_TWITCH_GREETING') {
		try {
			generateList(JSON.parse(data.data))
		} catch(e) {
			console.log(e)
		}
	} else if(data.event == 'EVENT_CONNECTED') {
		statusOutput.innerText = data.data.message
	}
}
socket.onclose = function () {
	statusOutput.innerText = 'Connection was closed. This might be due to an inalid API key. Please reset it by right-clicking the script and Insert API key. Refresh or re-open window afterwards.'
}