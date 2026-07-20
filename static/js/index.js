window.addEventListener("load", function(){

    const loader = document.getElementById("loader");

    loader.style.opacity = "0";

    setTimeout(function(){

        loader.style.display = "none";

    },500);

});

const modal = document.getElementById("introModal");
const openBtn = document.getElementById("openIntro");
const closeBtn = document.getElementById("closeIntro");
const video = document.getElementById("introVideo");

openBtn.addEventListener("click", () => {
    modal.style.display = "flex";
});

closeBtn.addEventListener("click", () => {
    modal.style.display = "none";
    video.pause();
    video.currentTime = 0;
});

window.addEventListener("click", (e) => {
    if (e.target === modal) {
        modal.style.display = "none";
        video.pause();
        video.currentTime = 0;
    }
});