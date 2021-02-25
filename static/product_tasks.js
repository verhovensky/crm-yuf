// sending a csrftoken with every ajax request
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", document.cookie.replace('csrftoken=', ''));
        }
    }
});


//Get productID and store in localStorage
$( ".get_delete_id" ).on( "click", function() {
var productID = $(this).attr("data-id");
console.log(productID);
window.localStorage.setItem('item', productID);
});

$( ".delete_button_id" ).on( "click", function() {
var productID = window.localStorage.getItem('item');
// Check if (productID) exists
$.ajax({
  url: "delete/" + productID,
  type: 'POST',
  success: function(data) {
    $("#exampleModalCenter").modal("hide");
    $("#deleteSuccessModal").modal("show");
    // Get the element by which we find nearest
    x = $("[data-id='" + productID + "']");
    x.closest("figure").addClass("bg-danger");
    x.closest("figure").hide(2000);
    console.log("Successfully deleted! )))");
    window.localStorage.removeItem("item");
    }
  }
});
});