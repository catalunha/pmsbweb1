function remover_mascaras(form) {
    $(form).find(':input[class*="-mask"]').unmask();
}
// fazer uma versão em jquery
function myFunction() {
        var input, filter, ul, li, a, i;
        input = document.getElementById("myInput");
        filter = input.value.toUpperCase();
        div = document.getElementsByClassName("thread");
        user = document.getElementsByClassName("participants")
        console.log(ul);
        for (i = 0; i < div.length; i++) {
            a = user[i].innerText;
            console.log(a);
            if (a.toUpperCase().indexOf(filter) > -1) {
                div[i].style.display = "";
            } else {
                div[i].style.display = "none";
            }
        }
    }