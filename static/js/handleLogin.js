
document.querySelector("#loginForm")
.addEventListener("submit", (e)=>{
    e.preventDefault()
    let valid = true
    document.querySelectorAll(".required").forEach(element =>{
        const PARENTNODE = element.parentElement;
        let userProps = PARENTNODE.querySelector("input").value;
        if (userProps <= 0){
            valid = false
            PARENTNODE.querySelector(".err-div").classList.remove("hidden")
        }
        else{
            valid =true
            PARENTNODE.querySelector(".err-div").classList.add("hidden")    
        }
    })
    let csrfToken =  getCookies("csrftoken")
    $.ajax({
        url:"/user/login/",
        type:"POST",
        data:{
            "username" : e.target.username.value,
            "password" : e.target.password.value,
            csrfmiddlewaretoken: csrfToken
        },
        success:(res)=>{
            if(res["status"]){
                $(location).attr("href","/home/")
            }
            else{
                document.querySelector(".login-err-div").classList.remove("hidden")
            }
        },
    })
})