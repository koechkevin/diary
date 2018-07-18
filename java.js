function validateForm() {
    var f = document.forms["register"]["fname"].value;
    var l = document.forms["register"]["lname"].value;
    var e = document.forms["register"]["email"].value;
    var u = document.forms["register"]["username"].value;
    var p = document.forms["register"]["password"].value;
    var cp = document.forms["register"]["cpassword"].value;
    var atIndex=e.indexOf("@");
    var dotIndex=e.lastIndexOf(".");
    
    if (f == ""||l == ""||u == ""||p == ""||cp == "") {
        alert("All fields must be filled out");
        return false;
    }
    else if (atIndex<1 || dotIndex-atIndex < 2) {
        alert("invalid email");
        document.register.email.focus() ;
        return false;
    }
}
function validateLogin() {
    var u = document.forms["login"]["username"].value;
    var p = document.forms["login"]["password"].value;
    if (u == "") {
        alert("username cannot be empty");
        document.login.username.focus() ;
        return false;
    }
    else if (p == "") {
        alert("password cannot be empty");
        document.login.password.focus() ;
        return false;
    }   
    
} 
var modal = document.getElementById('myModal');
var btn = document.getElementById("myBtn");
var span = document.getElementsByClassName("close")[0];
btn.onclick = function() {
    modal.style.display ="block";
}
span.onclick = function() {
    modal.style.display = "none";
}
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}







