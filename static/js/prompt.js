function submitPrompt() {
  var promptInput = document.getElementById("prompt-input");
  var promptText = promptInput.value;
  var image = document.getElementById("image");
  var imagePath = image.src;


  fetch("/process_text", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ "image_path": imagePath , "prompt": promptText}),
  })
    .then(function (response) {
      return response.blob();
    })
    .then(function (blob) {
      promptText = "";
    });
}