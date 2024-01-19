function onInputFileChange() {
    var file = document.getElementById('file').files[0];
    var url = URL.createObjectURL(file);
    var name = document.getElementById('file').files[0];
    console.log(url);
    document.getElementById("video_id").src = url;
    document.getElementById("print") = name;
}