function openEditModal(button) {

    document.getElementById("editModal").style.display = "block";

    document.getElementById("editTitle").value = button.dataset.title;
    document.getElementById("editCategory").value = button.dataset.category;
    document.getElementById("editDescription").value = button.dataset.description;

    document.getElementById("editForm").action = "/edit/" + button.dataset.id;
}

function closeEditModal(){

    document.getElementById("editModal").style.display = "none";

}