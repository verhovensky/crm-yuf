// Function to get CSRF token value from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// sending a csrftoken with every ajax request
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


//Get pk and store in localStorage
$( ".get_delete_id" ).on( "click", function() {
var orderID = $(this).attr("data-id");
window.localStorage.setItem('item', orderID);
console.log(orderID);
});

$( ".delete_button_id" ).on( "click", function() {
var orderID = window.localStorage.getItem('item');
// Check if order exists
$.ajax({
  url: "delete/" + orderID,
  type: 'POST',
  success: function(data) {
    $("#OrderModalCenter").modal("hide");
    $("#deleteSuccessModal").modal("show");
    // Get the element by which we find nearest
    x = $("[data-id='" + orderID + "']");
    console.log(x);
    x.closest("tr").addClass("bg-danger");
    x.closest("tr").hide(2000,
        function(){
            this.remove();
        });
    window.localStorage.removeItem("item");
    }
  });
});