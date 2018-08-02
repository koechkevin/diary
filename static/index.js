function fetchIndex(){
fetch("http://127.0.0.1:5013/api/v2").then(function(response){
    if (!response.ok) {
    throw Error(response.statusText);
  }
    else{
    console.log(response.json());
    }
})
}
function fetchRegister(){
    var url = "http://127.0.0.1:5013/api/v2/users/register"
    var fname = document.getElementById("fname")
    var lname = document.getElementById("lname")
    var username = document.getElementById("username")
    var email = document.getElementById("email")
    var password = document.getElementById("password")
    var cpassword = document.getElementById("cpassword")
    var data = {"fname":fname,"lname":lname, "username":username, "email":email,
               "password":password, "cpassword":cpassword}
    fetch(url, {method: 'POST',
         body: JSON.stringify(data),
        headers:{
    'Content-Type': 'application/json'
        }
  }).then(function(response){
      if (!response.ok){}
      else {
      console.log(response.json());
      }
  }
  )}
