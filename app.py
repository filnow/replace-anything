import cv2
import io
import glob
import argparse

from flask import Flask, render_template, send_from_directory, send_file, request
from sam import SAM
from diffusion import SD


parser = argparse.ArgumentParser()
parser.add_argument('--model', 
                    help='The model to use', 
                    choices=['vit_l', 'vit_b', 'vit_h'], 
                    required=True)
parser.add_argument('--inpainting', 
                    help='Use inpainting', 
                    action='store_true')
args = parser.parse_args()

print(f"Using model: {args.model}\n")
print(f"Using inpainting: {args.inpainting}\n")

app = Flask(__name__, static_folder='static')
seg = SAM(model=args.model)

@app.route('/')
def gallery():
    images = glob.glob('./static/images/*')
    return render_template('gallery.html', images=images)

@app.route('/images/<path:filename>')
def image(filename):
    return render_template('image.html', image_path='/'+filename)

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
    seg.get_mask([[x, y]])
  
    mask = cv2.resize(seg.mask_to_show(), (display_width, display_height))
    _, buffer = cv2.imencode('.jpg', mask)
    buffered = io.BytesIO(buffer)
    buffered.seek(0)

    return send_file(buffered, mimetype="image/jpeg")

@app.route("/process_text", methods=["POST"])
def process_text():
    
    data = request.get_json()

    if args.inpainting and seg.img != None:
        sd = SD()
        image = cv2.resize(seg.img, (512,512))
        prompt = request.form.get("prompt").lower()
        mask = seg.mask_for_sd()
        generated_img = sd.generate_for_mask(image, mask, prompt)

        _, buffer = cv2.imencode('.jpg', generated_img)
        buffered = io.BytesIO(buffer)
        buffered.seek(0)

        return send_file(buffered, mimetype="image/jpeg")
  
    image = cv2.imread('./static/images/' + data['image_path'].split('/')[-1])

    _, buffer = cv2.imencode('.jpg', image)
    buffered = io.BytesIO(buffer)
    buffered.seek(0)

    return send_file(buffered, mimetype="image/jpeg")

@app.route("/preview")
def previw():
    return render_template("preview.html", gif_path="/static/assets/ra-preview.gif")

if __name__ == '__main__':
    app.run(debug=True)