function fetchIndex(){
fetch("http://127.0.0.1:5013/api/v2/", {method:"GET", 
headers:{"Content-Type":"application/json"}})
.then((response) => response.json())
.then((data)=>{
    document.getElementById("output").innerHTML = data["message"]
})
.catch((err) => console.log(err))
}

function fetchRegister(){
    event.preventDefault()
    var url = "http://localhost:5013/api/v2/users/register"
    var firstname = document.forms["register"]["fname"].value;
    var lastname = document.forms["register"]["lname"].value;
    var name = document.forms["register"]["username"].value;
    var emailaddress = document.forms["register"]["email"].value;
    var pasword = document.forms["register"]["password"].value;
    var confirmpassword = document.forms["register"]["cpassword"].value;
    var data = {fname:firstname,lname:lastname, username:name, email:emailaddress,
               password:pasword, cpassword:confirmpassword};                    
    fetch(url, {method:"POST", 
    headers:{
        "Content-Type":"application/json"
}, 
body:JSON.stringify(data)
    }).then((res)=>res.json())
    .then((data) => console.log(data))
    .catch((err) => console.log('error:',err));
    
        }
function fetchAccount(){
    event.preventDefault()
    const url = "http://127.0.0.1:5013/api/v2/users/register"
    fetch(url, {method:"GET",
headers: {"Content-Type":"application/json", 'x-access-token':"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMywidXNlcm5hbWUiOiJraWJpdG9rIiwiZXhwIjoxNTMzNzQ2NzE4fQ.VD4-Rsummo-HKHtZ5Cyl6NAzwn1kNlYU2OsK_rwadjQ"}})
.then((resp)=>resp.json())
.then((data) => console.log(data))
.catch(error => console.log('error:',error));
}
function fetchLogin(){
    event.preventDefault()
    var url = "http://127.0.0.1:5013/api/v2/users/login"
    var user = document.forms["login"]["username"].value;
    var pass = document.forms["login"]["password"].value;
    var data = {username:user, password:pass};
    fetch(url, {method:"POST", 
    headers:{
        "Content-Type":"application/json"
}, 
body:JSON.stringify(data)
    })
    .then((res)=>res.json())
    .then((data) => console.log(data))
    .catch(error => console.log('error:',error));

}
function fetchNewEntry(){
    event.preventDefault()
    let url = "http://127.0.0.1:5013/api/v2/entries"
    let titl = document.forms["create"]["title"].value;
    let entr = document.forms["create"]["entry"].value;
    let data = {title:titl, entry:entr}
    fetch(url, {method:"POST",
    headers: {"Content-Type":"application/json", 'x-access-token':""},
    body:JSON.stringify(data)
}).then((response) => response.json())
.then((output)=>console.log(output))
.catch((err)=>console.log(err))
}