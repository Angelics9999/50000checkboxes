document.addEventListener("DOMContentLoaded", function() {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    var checkboxes = document.querySelectorAll(".checkbox");

    // Fetch the initial state of checkboxes
    fetch('/state').then(response => response.json()).then(state => {
        state.forEach((checked, index) => {
            checkboxes[index].checked = checked;
        });
    });

    // When a checkbox is clicked
    checkboxes.forEach((checkbox, index) => {
        checkbox.addEventListener('change', function() {
            socket.emit('checkbox_click', { id: index, checked: checkbox.checked });
        });
    });

    // Update checkboxes in real-time when another user clicks
    socket.on('update_checkbox', function(data) {
        checkboxes[data.id].checked = data.checked;
    });

    // When all checkboxes are checked
    socket.on('all_checked', function() {
        alert('All 1000 checkboxes have been selected! The game is over.');
        checkboxes.forEach(checkbox => checkbox.disabled = true);
    });
});
