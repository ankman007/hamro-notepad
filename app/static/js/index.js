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

function deleteNote(noteId){
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId })
    }).then((_res) => {
        window.location.href = "/"
    });
}