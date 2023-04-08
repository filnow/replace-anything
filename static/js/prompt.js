function submitPrompt() {
  var promptInput = document.getElementById("prompt-input");
  var promptText = promptInput.value;

  fetch("/process_text", {
    method: "POST",
    body: new FormData(document.getElementById("prompt-form")),
  })
    .then(function (response) {
      return response.text();
    })
    .then(function (processedText) {
      console.log(processedText);
      // Do something with the processed text, like display it on the page
    });
}