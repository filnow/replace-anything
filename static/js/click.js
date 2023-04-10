window.onload = function() {
    var img = document.getElementById("image");
    img.dataset.src = img.src;

    img.onclick = async (e) => {
        var x = e.offsetX;
        var y = e.offsetY;
        var width = e.target.clientWidth;
        var height = e.target.clientHeight;
        var image_path = e.target.dataset.src;
        console.log("Clicked at: (" + x + ", " + y + ")");
        var data = { "x": x, "y": y, "image_path": image_path, "width": width, "height": height };
        var response = await fetch('/get_coords', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        var buffer = await response.arrayBuffer();

        // Create a new blob object from the buffer data
        var blob = new Blob([buffer], { type: 'image/jpeg' });
        // Replace src with the new one
        e.target.src = URL.createObjectURL(blob);
    }
}
