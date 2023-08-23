$(document).ready(function() {
    var alert_content = document.getElementsByClassName("alert-content");
    var error_alert = document.getElementById("error-alert");
    var success_alert = document.getElementById("success-alert");

    function showAlert(msg = "", warning = true) {
        if (msg) {
            for (var i = 0; i < alert_content.length; i++) {
                alert_content[i].textContent = msg;
            }
            if (warning) {
                error_alert.style.display = "block";
                setTimeout(function () {
                    error_alert.style.display = "none";
                }, 5000);
            } else {
                success_alert.style.display = "block";
                setTimeout(function () {
                    success_alert.style.display = "none";
                }, 5000);
            }
        }
    };

    $(".close-alert").click(function() {
        $(this)
            .parent(".alert")
            .fadeOut();
    });

    // var closeButtons = document.getElementsByClassName("close-alert");
    // if (closeButtons.length > 0) {
    //     setTimeout(function() {
    //         for (var i = 0; i < closeButtons.length; i++) {
    //             closeButtons[i].click();
    //         }
    //     }, 5000);
    // }
    
});
