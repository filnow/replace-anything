from flask import Flask, render_template, send_from_directory, request
from sam import SAM
import cv2
import matplotlib.pyplot as plt
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
    mask = seg.mask_to_show()
    cv2.imwrite('./output/image.jpg', mask)


if __name__ == '__main__':
    app.run(debug=True)