function openModal(card){

    const title = card.dataset.title;
    const prompt = card.dataset.prompt || "No prompt available";
    const file = card.dataset.file;
    const type = card.dataset.type;
    const youtube = card.dataset.youtube;

    document.getElementById("promptModal").style.display = "block";
    document.getElementById("modalTitle").innerText = title;
    document.getElementById("modalPrompt").innerText = prompt;

    const media = document.getElementById("modalMedia");

    if(type === "image"){

    media.innerHTML = `
        <img src="${file}" id="modalImage">
    `;

}
else if(type === "video"){

    media.innerHTML = `
        <video controls autoplay style="width:100%;border-radius:15px;">
            <source src="${file}" type="video/mp4">
        </video>
    `;

}
else if(type === "youtube"){

    let embed = youtube;

    if(embed.includes("watch?v=")){
        embed = embed.replace("watch?v=","embed/");
    }

    if(embed.includes("youtu.be/")){
        embed = embed.replace("youtu.be/","youtube.com/embed/");
    }

    media.innerHTML = `
        <iframe
            width="100%"
            height="500"
            src="${embed}"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
            style="border-radius:15px;">
        </iframe>
    `;

}

}
function closeModal(){

    let video = document.querySelector("#modalMedia video");

    if(video){

        video.pause();

        video.removeAttribute("src");

        video.load();

    }

    document.getElementById("promptModal").style.display = "none";

}

function copyPrompt() {
    let text = document.getElementById("modalPrompt").innerText;
    navigator.clipboard.writeText(text);
    alert("Prompt copied!");
}

function filterCards(category) {

    let cards = document.querySelectorAll(".card");
    let visible = 0;

    cards.forEach(card => {

        if (category === "all") {
            card.style.display = "block";
            visible++;
            return;
        }

        if (card.dataset.category === category) {
            card.style.display = "block";
            visible++;
        } else {
            card.style.display = "none";
        }

    });

    const empty = document.getElementById("empty-message");

    if (visible === 0) {
        empty.style.display = "block";
    } else {
        empty.style.display = "none";
    }

}

window.onclick = function(event) {
    let modal = document.getElementById("promptModal");
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

window.addEventListener("load", function(){

    const loader = document.getElementById("loader");

    loader.style.opacity = "0";

    setTimeout(function(){

        loader.style.display = "none";

    },500);

});
