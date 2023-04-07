window.onload = function() {
    var img = document.getElementById("image");
  
    img.onclick = function(e) {
      var x = e.offsetX;
      var y = e.offsetY;
      console.log("Clicked at: (" + x + ", " + y + ")");
    }
  }