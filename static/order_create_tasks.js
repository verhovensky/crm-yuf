// Hide all the fields on form initial load
$("#id_full_name").hide();
$("#id_address").hide();
$("#id_phone").hide();


$("#id_new_client").change(function() {
    if ($(this).prop('checked')) {
        $("#id_this_order_client").prop('checked', '').hide();
        $('label[for="id_for_other"]').hide();
        $('label[for="id_this_order_client"]').hide();
        $("#id_for_other").hide();
        $("#id_full_name").show();
        $("#id_address").show();
        $("#id_phone").show();
    } else {
        // console.log($(this).prop('checked'));
        $("#id_full_name").hide();
        $("#id_address").hide();
        $("#id_phone").hide();
        $("#id_for_other").show();
        $('label[for="id_for_other"]').show();
        $("#id_this_order_client").show();
        $('label[for="id_this_order_client"]').show();
    }
});


$("#id_for_other").change(function() {
    if ($(this).prop('checked')) {
        $("#id_new_client").prop('checked', false).hide();
        $('label[for="id_new_client"]').hide();
        $("#id_full_name").show();
        $("#id_address").show();
        $("#id_phone").show();
    } else {
        // console.log($(this).prop('checked'));
        $("#id_new_client").hide();
        $("#id_address").hide();
        $("#id_phone").hide();
        $("#id_full_name").hide();
        $("#id_new_client").show();
        $('label[for="id_new_client"]').show();
    }
});