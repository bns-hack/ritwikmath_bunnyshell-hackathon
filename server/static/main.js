document.querySelector('#plan-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    // Get the form input values
    var currency = document.getElementById('currency').value;
    var name = document.getElementById('name').value;
    var amount = document.getElementById('amount').value;

    // Get the selected payment gateways
    var paymentGateways = Array.from(document.querySelectorAll('input[name="paymentMethod"]:checked'))
    .map(function(checkbox) {
        return checkbox.value;
    })
    .join(',');

    if (paymentGateways == "" || paymentGateways == null) {
        alert("Please select atleast one Payment Gateway")
        return
    }

    // Create an object with the data
    var data = {
        currency: currency,
        name: name,
        price: parseFloat(amount),
        gateway: paymentGateways
    };

    // Check if access_token is available in cookies
    var access_token = document.cookie.replace(/(?:(?:^|.*;\s*)access_token\s*\=\s*([^;]*).*$)|^.*$/, "$1");

    // Send the POST request with the access_token as a bearer token
    fetch('api/plans', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + access_token // Include the access_token as a bearer token
        },
        body: JSON.stringify(data)
    })
    .then(function(response) {
        if (response.ok) {
            // Request successful, display success modal
            var successModal = new bootstrap.Modal(document.getElementById('successModal'));
            var successMessage = document.getElementById('successMessage');
            successMessage.textContent = "Plan created successfully";
            successModal.show();
            populateTbale()
        } else {
            // Request failed, display error modal
            var errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
            var errorMessage = document.getElementById('errorMessage');
            response.text().then(function(text) {
                if (response.status === 400)
                    errorMessage.textContent = JSON.parse(text).error;
                else
                    errorMessage.textContent = "Plan creation failed";
                errorModal.show();
            });
        }
    })
    .catch(function(error) {
        console.error('Error:', error);
    });
});


const plan_table = document.querySelector('#plan-table-body')

if (plan_table) {
    populateTbale()
}

function populateTbale() {
    var access_token = document.cookie.replace(/(?:(?:^|.*;\s*)access_token\s*\=\s*([^;]*).*$)|^.*$/, "$1");

    // Send the GET request with the access_token as a bearer token
    fetch('api/plans', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + access_token // Include the access_token as a bearer token
        }
    })
    .then(function(response) {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Error: ' + response.status);
        }
    })
    .then(function(data) {
        var planTableBody = document.getElementById('plan-table-body');

        // Clear existing table rows
        planTableBody.innerHTML = '';

        // Populate the table with the received plan data
        data.data.forEach(function(plan) {
            var row = document.createElement('tr');
            row.innerHTML = '<td>' + plan.name + '</td>' +
                            '<td>' + plan.price + '</td>' +
                            '<td>' + plan.currency + '</td>' +
                            '<td>' + plan.gateway + '</td>';
            planTableBody.appendChild(row);
        });
    })
    .catch(function(error) {
        console.error('Error:', error);
    });
}