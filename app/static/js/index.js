function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/view-notes";
  });
}

function confirmDelete(noteId) {
  if (confirm("Are you sure you want to delete this note?")) {
    deleteNote(noteId);
  }
}

function editNote(noteId) {
  const url = `/edit-note/${noteId}`;
  const data = {
    title: document.getElementById("title").value,
    content: document.getElementById("content").value,
  };
  console.log('url', url);
  console.log('data', data);
  fetch(url, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.msg) {
        window.location.href = `/view-notes?nocache=${new Date().getTime()}`;
      }
    })
    .catch((error) => console.error("Error:", error));
}

document.addEventListener("DOMContentLoaded", function () {
  function formatDate(dateString) {
    const options = { year: "numeric", month: "short", day: "numeric" };
    const date = new Date(dateString);
    return date.toLocaleDateString(undefined, options);
  }

  document.querySelectorAll(".note-date").forEach(function (element) {
    const rawDate = element.getAttribute("data-date");
    element.textContent = formatDate(rawDate);
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const noteContent = document.getElementById("noteContent");
  const noteTitle = document.getElementById("noteTitle");
  const editButton = document.getElementById("editButton");
  const saveButton = document.getElementById("saveButton");
  const cancelButton = document.getElementById("cancelButton");

  editButton.addEventListener("click", function () {
    noteContent.removeAttribute("readonly");
    noteTitle.removeAttribute("readonly");
    noteContent.focus();
    editButton.classList.add("d-none");
    saveButton.classList.remove("d-none");
    cancelButton.classList.remove("d-none");
  });

  cancelButton.addEventListener("click", function () {
    noteContent.setAttribute("readonly", "readonly");
    noteTitle.setAttribute("readonly", "readonly");
    editButton.classList.remove("d-none");
    saveButton.classList.add("d-none");
    cancelButton.classList.add("d-none");
    noteContent.value = "{{ note.content }}";
    noteTitle.value = "{{ note.title }}";
  });

  document
    .getElementById("noteForm")
    .addEventListener("submit", function (event) {
      event.preventDefault();

      alert("Note saved!");
      noteContent.setAttribute("readonly", "readonly");
      noteTitle.setAttribute("readonly", "readonly");
      editButton.classList.remove("d-none");
      saveButton.classList.add("d-none");
      cancelButton.classList.add("d-none");
    });
});
