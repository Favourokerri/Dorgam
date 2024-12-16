//function for csrf token. from django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


const inputs = document.querySelectorAll("#quantity");
let total_price = document.getElementById("total_price");

inputs.forEach(input => {
    input.addEventListener("input", function (e) {
        let url = "/store/updateItem";
        let item_id = this.dataset.action;
        let data = { item_id: item_id, quantity: this.value };
        console.log(data);

        fetch(url, {
            method: "POST",
            headers: { "content-type": "application/json", 'X-CSRFToken': csrftoken },
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(data => {
            console.log(data.message);
            if (data.total_price){
                total_price.innerHTML = `N${data.total_price}`
            }
        });
    });
});

//shipping fee
 const stateSelect = document.getElementById('state');
 let shppingFee = document.getElementById('shippingFee');
 let shippingFeeInput = document.getElementById('shipping-fee');
    stateSelect.addEventListener('change', function() {
        let url = "/store/shippingFee";
        const selectedStateId = stateSelect.value;
        let data = { state_id: selectedStateId};

        fetch(url, {
            method: "POST",
            headers: { "content-type": "application/json", 'X-CSRFToken': csrftoken },
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(data => {
            console.log(data.message);
            shppingFee.innerHTML = `N${data.shippingFee}`
            shippingFeeInput.value = data.shippingFee
        });
    });