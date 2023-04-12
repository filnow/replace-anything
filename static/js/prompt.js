function submitPrompt() {
  var promptInput = document.getElementById("prompt-input");
  var promptText = promptInput.value;
  var image = document.getElementById("image");

  fetch("/process_text", {
    method: "POST",
    body: new FormData(document.getElementById("prompt-form")),
  })
    .then(function (response) {
      return response.blob();
    })
    .then(function (blob) {
      image.src = URL.createObjectURL(blob);
      promptText = "";
    });
}
