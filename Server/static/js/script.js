function promptPassword() {
    var password = prompt("Enter the password:");

    if (password !== null) {
        // Send the password to the Flask server using fetch
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ password: password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                alert(data.message); // Show success message
                window.location.reload()
            } else {
                alert(data.message); // Show failure message
                window.location.reload()
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was an error connecting to the server.');
        });
    }
}

function relayMessage(msg){
    alert(msg)
}

