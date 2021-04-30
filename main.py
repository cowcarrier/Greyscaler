from flask import Flask, render_template, redirect, request,send_file
from flask.helpers import url_for
from werkzeug.utils import secure_filename
import os
from processor import processor


app = Flask(__name__)
UPLOAD_FOLDER = './static/process/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('home.html', message='GREY SCALER')


@app.route('/process/', methods=['POST', 'GET'])
def process():
    f = request.files['file'] 
    if f.filename == '':
        return render_template('home.html', message='ADD A FILE')
    if f.filename[f.filename.find('.')+1::] in app.config['ALLOWED_EXTENSIONS']:
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        processor(f.filename)
        return redirect(url_for('download',filename=f.filename))
    else:
        return render_template('home.html', message='NOT AN IMG FILE')
    

@app.route('/download/<filename>')
def download(filename):
    filelocation = './static/process/'+filename
    return send_file(filelocation,as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
