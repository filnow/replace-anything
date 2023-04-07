from flask import Flask, render_template, send_from_directory, redirect, url_for
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

if __name__ == '__main__':
    app.run(debug=True)