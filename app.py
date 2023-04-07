from flask import Flask, render_template, send_from_directory, request
import glob

app = Flask(__name__, static_folder='static')

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
    x = data['x']
    y = data['y']
    image_path = data['image_path']
    print(x, y, image_path)
    #TODO: run model with input x,y here
    return 'Success'

if __name__ == '__main__':
    app.run(debug=True)