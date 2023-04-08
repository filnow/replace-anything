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
            return response.arrayBuffer();
        }).then(function(buffer) {
            // Create a new blob object from the buffer data
            var blob = new Blob([buffer], { type: 'image/jpeg' });
        
            // Create an image element and set its src attribute to the blob data URL
            var img = new Image();
            img.src = URL.createObjectURL(blob);
        
            // Replace the original image with the modified image
            var oldImg = document.getElementById('image');
            oldImg.parentNode.replaceChild(img, oldImg);
        });
        
    }
  }
