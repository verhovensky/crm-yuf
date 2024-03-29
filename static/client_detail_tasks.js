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

// Redirect back to clients page
function pageRedirect() {
      window.location.href = window.location.origin + "/client/";
    }

//Get client pk and store in localStorage
$( ".get_delete_id" ).on( "click", function() {
var userID = $(this).attr("data-id");
window.localStorage.setItem('item', userID);
});

$( ".delete_button_id" ).on( "click", function() {
var userID = window.localStorage.getItem('item');
delUrl = window.location.origin + "/client/delete/";
console.log(delUrl);
// Check if (productID) exists
$.ajax({
  url: delUrl + userID,
  type: 'POST',
  success: function(data) {
    $("#ClientModalCenter").modal("hide");
    $("#deleteSuccessModal").modal("show");
    // Get the element by which we find nearest
    x = $("[data-id='" + userID + "']");
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