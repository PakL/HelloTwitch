function generateList(users) {
	var list = document.querySelector('#userlist')
	list.innerHTML = ''

	for(var u in users) {
		if(!users.hasOwnProperty(u)) continue

		var user = users[u]
		var item = document.createElement('li')
		item.innerText = user
		list.appendChild(item)
	}
}