function openModal(card){

    const title = card.dataset.title;
    const prompt = card.dataset.prompt || "No prompt available";
    const file = card.dataset.file;
    const type = card.dataset.type;

    document.getElementById("promptModal").style.display = "block";
    document.getElementById("modalTitle").innerText = title;
    document.getElementById("modalPrompt").innerText = prompt;

    const media = document.getElementById("modalMedia");

    if(type === "image"){

        media.innerHTML = `<img src="${file}" id="modalImage">`;

    }else{

        media.innerHTML = `
            <video controls autoplay style="width:100%;border-radius:15px;">
                <source src="${file}" type="video/mp4">
            </video>
        `;

    }

}
function closeModal() {
    document.getElementById("promptModal").style.display = "none";
}

function copyPrompt() {
    let text = document.getElementById("modalPrompt").innerText;
    navigator.clipboard.writeText(text);
    alert("Prompt copied!");
}

function filterCards(category) {

    let cards = document.querySelectorAll(".card");

    cards.forEach(card => {

        if (category === "all") {
            card.style.display = "block";
            return;
        }

        let cardCategory = card.getAttribute("data-category");

        if (cardCategory === category) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }

    });
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