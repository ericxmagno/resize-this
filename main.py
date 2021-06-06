import os
import sys
from flask.ctx import after_this_request

from flask.wrappers import Response
from io import BytesIO
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
from PIL import Image

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed below')
		return render_template('upload.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/download', methods=['POST'])
def download_reduced_image():
	filename = secure_filename(request.form['file'])
	file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
	
	im = Image.open(file)
	im_format = im.format
	reduced_size = request.form['imgSize']

	if reduced_size == '50p':
		im = im.resize((int(im.size[0]/2),int(im.size[1]/2)), 0)
	elif reduced_size == '25p':
		im = im.resize((int(im.size[0]/4),int(im.size[1]/4)), 0)

	return serve_pil_image(im, reduced_size, im_format)

def serve_pil_image(pil_img, new_size, format):
	filename = os.path.join(app.config['UPLOAD_FOLDER'], 'temp.' + format)
	pil_img.save(filename, format, quality=70)

	dump = BytesIO()
	with open(filename, 'rb') as fo:
		dump.write(fo.read())
	dump.seek(0)

	@after_this_request 
	def remove_file(response): 
		os.remove(filename) 
		return response 

	return send_file(dump, mimetype='image/jpeg', attachment_filename='reduced_image_'+new_size+'.'+format.lower(), as_attachment=True)

if __name__ == "__main__":
	app.run(debug=True)