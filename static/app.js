$(document).ready(function() {

    setInterval("ajaxd()",10000); // call every 10 seconds

});

function ajaxd() {
  //reload result into element with id "sysStatus"
  $("#items_holder").load("/check_response", function(result) {

    n = result.localeCompare('On')

    if (n === 0) {
  //  block of code to be executed if the condition is true

        alert('Task Completed Redirecting'+' '+result);

    }
    else{
        //pass
    }

});
}
