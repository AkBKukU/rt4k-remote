function command(event) {
	fetch("/command", {
		method: 'post',
	   headers: {
		   "Content-Type": "application/json",
		   'Accept':'application/json'
	   },
	   body: JSON.stringify({"cmd":event.target.attributes.name.nodeValue}),
	}).then(() => {
		// Do Nothing
	});
};

function command_keys(event) {
	switch (event.code)
	{
		case "ArrowLeft":
			cmd="remote left"
			break;
		case "ArrowUp":
			cmd="remote up"
			break;
		case "ArrowRight":
			cmd="remote right"
			break;
		case "ArrowDown":
			cmd="remote down"
			break;
		case "Enter":
			cmd="remote ok"
			break;
		case "Backspace":
			cmd="remote back"
			break;
		case "Escape":
			cmd="remote menu"
			break;
		default:
			return
	}


	fetch("/command", {
		method: 'post',
	   headers: {
		   "Content-Type": "application/json",
		   'Accept':'application/json'
	   },
	   body: JSON.stringify({"cmd":cmd}),
	}).then(() => {
		// Do Nothing
	});
};

this.addEventListener('keydown', command_keys)
