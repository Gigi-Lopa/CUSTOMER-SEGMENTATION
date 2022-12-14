/*GET COOOKIES*/ 
function getCookies(name){
    let cookieValues = null

    if(document.cookie && document.cookie !== ""){
        let cookies = document.cookie.split(";")
        for (var i = 0; i < cookies.length; i++){
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1 )=== (name + "=")){
                cookieValues = decodeURIComponent(cookie.substring(name.length + 1))
                break
            }
        }

    }
    return cookieValues
}