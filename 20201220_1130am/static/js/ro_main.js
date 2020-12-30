var input = document.getElementById("file_input")
var file_input_label = document.getElementById("file_input_label")

$(window).on("load", function () {
  $(".spinner-border").fadeOut("slow")
});

function input_filename() {
    file_input_label.innerText = input.files[0].name;
}

function upload() {
    let file = input.files[0];
    let filename = file.name;
    data.append('file', file);
}

function reset() {
    file_input_label.innerText = "Select file";
}