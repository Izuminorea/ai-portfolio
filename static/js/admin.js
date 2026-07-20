function openEditModal(button){

    document.getElementById("editModal").style.display = "block";

    document.getElementById("editTitle").value = button.dataset.title;
    document.getElementById("editCategory").value = button.dataset.category;
    document.getElementById("editDescription").value = button.dataset.description;

    document.getElementById("editFileType").value = button.dataset.type;

    // Kung walang YouTube URL, blanko lang
    document.getElementById("editYoutube").value = button.dataset.youtube || "";

    // Ipakita ang tamang input
    toggleEditMedia();

    document.getElementById("editForm").action = "/edit/" + button.dataset.id;

}
    function toggleMediaInput(){

    const type = document.getElementById("fileType").value;

    const uploadBox = document.getElementById("uploadBox");
    const youtubeBox = document.getElementById("youtubeBox");

    if(type === "youtube"){

        uploadBox.style.display = "none";
        youtubeBox.style.display = "block";

    }else{

        uploadBox.style.display = "block";
        youtubeBox.style.display = "none";

    }

}

window.onload = toggleMediaInput;
function closeEditModal(){

    document.getElementById("editModal").style.display = "none";

}
function toggleEditMedia(){

    const type = document.getElementById("editFileType").value;

    const uploadBox = document.getElementById("editUploadBox");
    const youtubeBox = document.getElementById("editYoutubeBox");

    if(type === "youtube"){

        uploadBox.style.display = "none";
        youtubeBox.style.display = "block";

    }else{

        uploadBox.style.display = "block";
        youtubeBox.style.display = "none";

    }

}