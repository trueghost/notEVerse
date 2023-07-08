// Get references to the search form and search input
const searchForm = document.getElementById('searchForm');
const searchInput = document.getElementById('searchInput');

// Add an event listener to the search form
searchForm.addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent form submission

    const searchTerm = searchInput.value.toLowerCase(); // Get the search term and convert to lowercase

    // Loop through each note container
    const noteContainers = document.querySelectorAll('.note-container');
    let matchedNotes = []; // Array to store the matched note containers

    noteContainers.forEach(function (noteContainer) {
        const noteTitle = noteContainer.querySelector('.note-title').textContent.toLowerCase();

        // Check if the note title includes the search term
        if (noteTitle.includes(searchTerm)) {
            matchedNotes.push(noteContainer); // Add the matched note container to the array
        } else {
            noteContainer.style.display = 'none'; // Hide non-matching note containers
        }
    });

    // Hide the search form
    searchForm.style.display = 'none';

    // Show the matched note containers and append them to the top
    const container = document.querySelector('.container');
    matchedNotes.forEach(function (noteContainer) {
        noteContainer.style.display = 'block';
        container.insertBefore(noteContainer, container.firstChild); // Append matched note container to the top
    });

    // Clear the search input
    searchInput.value = '';
});