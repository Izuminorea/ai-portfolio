window.addEventListener("load", function(){

    const loader = document.getElementById("loader");

    loader.style.opacity = "0";

    setTimeout(function(){

        loader.style.display = "none";

    },500);

});

const form = document.querySelector("form");
const sendBtn = document.getElementById("sendBtn");

form.addEventListener("submit", function(e){

    e.preventDefault();

    sendBtn.disabled = true;

    sendBtn.querySelector(".btn-text").textContent = "Sending...";

    sendBtn.querySelector(".spinner").style.display = "inline-block";

    setTimeout(() => {

        form.submit();

    }, 100);

});