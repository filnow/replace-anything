from flask import Flask, render_template, send_from_directory, send_file, request
from sam import SAM
import cv2
import io
from PIL import Image
import numpy as np
import glob

app = Flask(__name__, static_folder='static')
seg = SAM()

@app.route('/')
def gallery():
    images = glob.glob('./static/images/*')
    return render_template('gallery.html', images=images)

@app.route('/images/<path:filename>')
def image(filename):
    caption = filename.split('/')[-1]
    return render_template('image.html', image_path='/'+filename, caption=caption)

@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('static/images', filename)

@app.route('/get_coords', methods=['POST'])
def get_coords():
    data = request.get_json()
    
    display_width = data['width']
    display_height = data['height']
    
    image = cv2.imread('./static/images/' + data['image_path'].split('/')[-1])
    
    x = int(data['x'] * image.shape[1] / display_width)
    y = int(data['y'] * image.shape[0] / display_height)

    seg.set_image(image)
    seg.get_mask(np.array([[x, y]]))
    mask = cv2.cvtColor(seg.mask_to_show(), cv2.COLOR_BGR2RGB)

    pil_image = Image.fromarray(mask).resize((display_width, display_height))
    buffered = io.BytesIO()
    pil_image.save(buffered, format="JPEG")
    buffered.seek(0)

    return send_file(buffered, mimetype="image/jpeg")

@app.route("/process_text", methods=["POST"])
def process_text():
    text = request.form.get("prompt").lower()

    #TODO: stable diffusion here with this prompt
    
    return text

if __name__ == '__main__':
    app.run(debug=True)