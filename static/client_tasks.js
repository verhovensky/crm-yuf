// Function highlights row and deletes it
function DeleteRowAnim(element){
    element.closest("tr").addClass("bg-danger");
    element.closest("tr").hide(2000,
        function(){
            this.remove();

        });
}