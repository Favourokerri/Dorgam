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


//code for increase, decrease and remove
const inputs = document.querySelectorAll(".quantity");
inputs.forEach(input => {
    input.addEventListener("input", function (e) {
        console.log("input changed");
        // let product_id = e.target.value; // Access the "data-product-id" attribute
        let url = "/store/updateItem";
        let item_id = this.dataset.action;
        let data = { item_id: item_id };
        console.log(action);

        fetch(url, {
            method: "POST",
            headers: { "content-type": "application/json", 'X-CSRFToken': csrftoken },
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(data => {
            console.log(data);
            location.reload();
        });
    });
});