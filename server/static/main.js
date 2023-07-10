var stripe = Stripe('pk_test_51NRqEbBNDdJLcRKeDPg3WpT4Kkskd9m85v5Pz2fLh5RkyZa6WxUN8ojAo64uwN03A7SKMNBzqp3JVVQkl4uIzX3R00zJD2OX13');

let setup_intent = null;
let customer_data = null;

const plan_form = document.querySelector('#plan-form')

if (plan_form)
    plan_form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the form from submitting normally

        // Get the form input values
        var currency = document.getElementById('currency').value;
        var name = document.getElementById('name').value;
        var amount = document.getElementById('amount').value;

        // Get the selected payment gateways
        var paymentGateways = Array.from(document.querySelectorAll('input[name="paymentMethod"]:checked'))
            .map(function (checkbox) {
                return checkbox.value;
            })
            .join(',');

        if (paymentGateways == "" || paymentGateways == null) {
            var errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
            var errorMessage = document.getElementById('errorMessage');
            errorMessage.textContent = "Please select atleast one Payment Gateway";
            errorModal.show();
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
            .then(function (response) {
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
                    response.text().then(function (text) {
                        if (response.status === 400)
                            errorMessage.textContent = JSON.parse(text).error;
                        else
                            errorMessage.textContent = "Plan creation failed";
                        errorModal.show();
                    });
                }
            })
            .catch(function (error) {
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
        .then(function (response) {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Error: ' + response.status);
            }
        })
        .then(function (data) {
            var planTableBody = document.getElementById('plan-table-body');

            // Clear existing table rows
            planTableBody.innerHTML = '';

            // Populate the table with the received plan data
            data.data.forEach(function (plan) {
                var row = document.createElement('tr');
                row.innerHTML = '<td>' + plan.name + '</td>' +
                    '<td>' + plan.price + '</td>' +
                    '<td>' + plan.currency + '</td>' +
                    '<td>' + plan.gateway + '</td>';
                planTableBody.appendChild(row);
            });
        })
        .catch(function (error) {
            console.error('Error:', error);
        });
}

const customer = document.querySelector('#customer-detail')

if (customer) {
    populateCustomer()
}

function populateCustomer() {
    var access_token = document.cookie.replace(/(?:(?:^|.*;\s*)access_token\s*\=\s*([^;]*).*$)|^.*$/, "$1");

    // Fetch customer data from the API
    fetch('api/me', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + access_token // Include the access_token as a bearer token
        }
    })
        .then(function (response) {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Error: ' + response.status);
            }
        })
        .then(function (data) {
            if (data.data === null) {
                // Customer data is null, show the customer form instead of the card
                document.getElementById('customer-form').style.display = 'block';
                document.getElementById('customer-detail').style.display = 'none';
            } else {
                // Customer data is available, populate the card with the customer details
                document.getElementById('customer-form').style.display = 'none';
                document.getElementById('customer-detail').style.display = 'block';
                document.getElementById('customer-name').textContent = data.data.name;
                document.getElementById('customer-email').textContent = data.data.email;
                document.getElementById('customer-id').textContent = data.data.gateway_cust_id;
                populateSubscriptionTable()
            }
        })
        .catch(function (error) {
            console.error('Error:', error);
        });
}

document.querySelector('#customer-details-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the form from submitting normally

    var access_token = document.cookie.replace(/(?:(?:^|.*;\s*)access_token\s*\=\s*([^;]*).*$)|^.*$/, "$1");

    // Get the form input values
    var name = document.getElementById('customer-name-input').value;
    var country = document.getElementById('customer-country-input').value;
    var gateway = document.querySelector('input[name="paymentMethod"]:checked').value;

    // Create an object with the data
    var data = {
        name: name,
        country: country,
        gateway: gateway
    };

    // Send the POST request
    fetch('api/customers', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${access_token}`
        },
        body: JSON.stringify(data)
    })
    .then(function (response) {
        if (response.ok) {
            // Request successful, do something with the response
            var successModal = new bootstrap.Modal(document.getElementById('successModal'));
            var successMessage = document.getElementById('successMessage');
            successMessage.textContent = "Customer saved successfully";
            successModal.show();
            populateCustomer()
        } else {
            // Request failed, handle the error
            var errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
            var errorMessage = document.getElementById('errorMessage');
            response.text().then(function (text) {
                if (response.status === 400)
                    errorMessage.textContent = JSON.parse(text).error;
                else
                    errorMessage.textContent = "Plan creation failed";
                errorModal.show();
            });
        }
    })
    .catch(function (error) {
        console.error('Error:', error);
    });
});


const subscription = document.querySelector('#subscription-table-body')

if (subscription) {
    populateSubscriptionTable()
}

function populateSubscriptionTable() {
    if (document.getElementById('customer-detail').style.display == 'none') return;
    var access_token = document.cookie.replace(/(?:(?:^|.*;\s*)access_token\s*\=\s*([^;]*).*$)|^.*$/, "$1");

    // Fetch customer data from the API
    fetch('api/subscriptions', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + access_token // Include the access_token as a bearer token
        }
    })
    .then(function (response) {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Error: ' + response.status);
        }
    })
    .then(function (data) {
        if (data.data.length < 1) {
            document.getElementById('subscription-list').style.display = 'none';
            document.getElementById('subscription-form').style.display = 'block';
            populatePlansSelectionTbale()
            setSetupIntent()
        } else {
            let active = data.data.find(subs => subs.status == 'active')
            var subscriptionTableBody = document.getElementById('subscription-table-body');
            document.getElementById('subscription-list').style.display = 'block';
            if (!active) {
                document.getElementById('subscription-form').style.display = 'block';
                populatePlansSelectionTbale()
                setSetupIntent()
            } else {
                document.getElementById('subscription-form').style.display = 'none';
            }
            // Clear existing table rows
            subscriptionTableBody.innerHTML = '';

            // Populate the table with the received plan data
            data.data.forEach(function (subscription) {
                var row = document.createElement('tr');
                row.innerHTML = '<td>' + subscription.plan_name + '</td>' +
                    '<td>' + subscription.amount + '</td>' +
                    '<td>' + subscription.currency + '</td>' +
                    '<td>' + subscription.gateway + '</td>' +
                    '<td>' + 
                    `${subscription.status == 'active' ? '<button type="button" class="btn btn-danger btn-sm" onclick="cancelSubscription(' + subscription.id + ')">Cancel</button>': `Ending on ${subscription.cancel_at}`}` + 
                    '</td>';
                    subscriptionTableBody.appendChild(row);
            });
        }
    })
    .catch(function (error) {
        console.error('Error:', error);
    });
}

function populatePlansSelectionTbale() {
    var access_token = document.cookie.replace(/(?:(?:^|.*;\s*)access_token\s*\=\s*([^;]*).*$)|^.*$/, "$1");

    // Send the GET request with the access_token as a bearer token
    fetch('api/plans', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + access_token // Include the access_token as a bearer token
        }
    })
    .then(function (response) {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Error: ' + response.status);
        }
    })
    .then(function (data) {
        var planTableBody = document.getElementById('plan-selection-table-body');

        // Clear existing table rows
        planTableBody.innerHTML = '';

        // Populate the table with the received plan data
        data.data.forEach(function (plan) {
            var row = document.createElement('tr');
            row.innerHTML = '<td><input type="radio" name="subscription" value="' + plan.id + '"></td>' +
                '<td>' + plan.name + '</td>' +
                '<td>' + plan.price + '</td>' +
                '<td>' + plan.currency + '</td>' +
                '<td>' + plan.gateway + '</td>';
            planTableBody.appendChild(row);
        });
    })
    .catch(function (error) {
        console.error('Error:', error);
    });
}

async function setSetupIntent() {
    var access_token = document.cookie.replace(/(?:(?:^|.*;\s*)access_token\s*\=\s*([^;]*).*$)|^.*$/, "$1");

    // Send the GET request with the access_token as a bearer token
    response  = await fetch('api/customers/setup-intent', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + access_token // Include the access_token as a bearer token
        }
    })
    let data = null
    if (response.ok) {
        data = await response.json();
    } else {
        throw new Error('Error: ' + response.status);
    }
    if (data.data != null)
        setup_intent = data.data
    var elements = stripe.elements({
        clientSecret: setup_intent.client_secret,
    });
    var elements = stripe.elements();
    var cardElement = elements.create('card');

    cardElement.mount('#card-element');

    const subscription_form = document.querySelector('#subscription-form')

    if (subscription_form)
        subscription_form.addEventListener('submit', function (event) {
            event.preventDefault()

            var subscriptionRadios = document.querySelectorAll('input[name="subscription"]');
            var plan_id = '';
            var selectedGateway = '';

            subscriptionRadios.forEach(function(radio) {
                if (radio.checked) {
                    plan_id = radio.value;
                    var row = radio.closest('tr');
                    var gatewayCell = row.querySelector('td:nth-child(5)');
                    selectedGateway = gatewayCell.textContent;
                }
            });

            if (plan_id == '' || plan_id == null) {
                var errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
                var errorMessage = document.getElementById('errorMessage');
                errorMessage.textContent = "Select a plan";
                errorModal.show();
                return
            }
            stripe
                .confirmCardSetup(setup_intent.client_secret, {
                    payment_method: {
                        card: cardElement,
                        billing_details: {
                            name: 'Jenny Rosen',
                        },
                    },
                })
                .then(function(result) {
                    // Handle result.error or result.setupIntent
                    var access_token = document.cookie.replace(/(?:(?:^|.*;\s*)access_token\s*\=\s*([^;]*).*$)|^.*$/, "$1");
                
                    // Create an object with the data
                    var data = {
                        plan_id: plan_id,
                        gateway: selectedGateway,
                        payment_method: result.setupIntent.payment_method
                    };

                    // Send the POST request b
                    fetch('api/subscriptions', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${access_token}`
                        },
                        body: JSON.stringify(data)
                    })
                        .then(function (response) {
                            if (response.ok) {
                                // Request successful, do something with the response
                                var successModal = new bootstrap.Modal(document.getElementById('successModal'));
                                var successMessage = document.getElementById('successMessage');
                                successMessage.textContent = "Subscription created successfully";
                                successModal.show();
                                populateCustomer()
                            } else {
                                // Request failed, handle the error
                                var errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
                                var errorMessage = document.getElementById('errorMessage');
                                response.text().then(function (text) {
                                    if (response.status === 400)
                                        errorMessage.textContent = JSON.parse(text).error;
                                    else
                                        errorMessage.textContent = "Subscription creation failed";
                                    errorModal.show();
                                });
                            }
                        })
                        .catch(function (error) {
                            console.error('Error:', error);
                        });
                });
        })
}

function cancelSubscription(id) {
    var access_token = document.cookie.replace(/(?:(?:^|.*;\s*)access_token\s*\=\s*([^;]*).*$)|^.*$/, "$1");

    // Send the POST request b
    fetch(`api/subscriptions/${id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${access_token}`
        }
    })
        .then(function (response) {
            if (response.ok) {
                // Request successful, do something with the response
                var successModal = new bootstrap.Modal(document.getElementById('successModal'));
                var successMessage = document.getElementById('successMessage');
                successMessage.textContent = "Subscription created successfully";
                successModal.show();
                populateCustomer()
                populateSubscriptionTable()
            } else {
                // Request failed, handle the error
                var errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
                var errorMessage = document.getElementById('errorMessage');
                response.text().then(function (text) {
                    if (response.status === 400)
                        errorMessage.textContent = JSON.parse(text).error;
                    else
                        errorMessage.textContent = "Subscription creation failed";
                    errorModal.show();
                });
            }
        })
        .catch(function (error) {
            console.error('Error:', error);
        });
}