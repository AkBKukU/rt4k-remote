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
