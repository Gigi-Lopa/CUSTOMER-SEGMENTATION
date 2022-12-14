document.querySelector("#createAccountForm")
.addEventListener("submit",(e)=>{
    document.querySelectorAll(".required").forEach(element =>{
        let PARENT = element.parentElement
        let ParentInput = PARENT.querySelector("input").value.length
        if (ParentInput <= 0 )
        {
            e.preventDefault()
            PARENT.querySelector(".err-div").classList.remove("hidden")
        }
        else{
            PARENT.querySelector(".err-div").classList.add("hidden")
        }
    })
    let usernameInput = e.target.username.value.length   
    if (usernameInput < 3 || usernameInput >= 15){
        e.preventDefault()
        document.querySelector("#username-err").classList.remove("hidden")
    }
    else{
        document.querySelector("#username-err").classList.add("hidden")

    }
    if (e.target.confirmPassword.value !== e.target.password.value){
        e.preventDefault()
        document.querySelector(".password-err").classList.remove("hidden")
    } 
    else{
        document.querySelector(".password-err").classList.add("hidden")
    }
})