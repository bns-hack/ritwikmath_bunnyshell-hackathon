document.querySelector('#subscription-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    // Get the form input values
    var email = document.getElementById('exampleInputEmail1').value;
    var password = document.getElementById('exampleInputPassword1').value;
    var checkbox = document.getElementById('exampleCheck1').checked;

    // Create an object with the data
    var data = {
        email: email,
        password: password,
        checkbox: checkbox
    };

    // Send the POST request
    fetch('/api/subscriptions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(function(response) {
        if (response.ok) {
            // Request successful, do something with the response
            console.log('POST request successful');
        } else {
            // Request failed, handle the error
            console.error('Error:', response.status);
        }
    })
    .catch(function(error) {
        console.error('Error:', error);
    });
});