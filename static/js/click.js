window.onload = function() {
    var img = document.getElementById("image");
  
    img.onclick = function(e) {
        var x = e.offsetX;
        var y = e.offsetY;
        var width = img.clientWidth;
        var height = img.clientHeight;
        var image_path = document.getElementById("image").src;
        console.log("Clicked at: (" + x + ", " + y + ")");
        var data = { "x": x, "y": y, "image_path": image_path, "width": width, "height": height };
        fetch('/get_coords', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
        }).then(function(response) {
        return response.text();
        }).then(function(text) {
        console.log(text);
        });
    }
  }
