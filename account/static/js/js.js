// **** ALERT REMOVE *****

$(document).ready(function () {

    window.setTimeout(function () {
        $(".alert").fadeTo(1000, 0).slideUp(1000, function () {
            $(this).remove();
        });
    }, 5000);

});

// **** SHOW PASSWORD *****

function showPword(passwordId, eyeId, eyeSlashId) {
    var x = document.getElementById(passwordId);
    var eye = document.getElementById(eyeId);
    var eyeSlash = document.getElementById(eyeSlashId);

    if (x.type === "password") {
        x.type = "text";
        eye.style.display = "block";
        eyeSlash.style.display = "none";
    } else {
        x.type = "password";
        eye.style.display = "none";
        eyeSlash.style.display = "block";
    }
}