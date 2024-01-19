document.getElementById('showFileNameButton').addEventListener('click', function() {
    var fileInput = document.getElementById('fileInput');
    var fileName = fileInput.files[0].name;
    document.getElementById('fileNameDisplay').textContent = fileName;
});