const form = document.querySelector("form");

const btn = document.getElementById("loginBtn");

form.addEventListener("submit",function(){

    btn.disabled = true;

    btn.querySelector(".btn-text").textContent = "Signing in...";

    btn.querySelector(".spinner").style.display = "inline-block";

});