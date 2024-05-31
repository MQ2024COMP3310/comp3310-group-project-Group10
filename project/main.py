from flask import (
  Blueprint, render_template, request, 
  flash, redirect, url_for, send_from_directory, 
  current_app, make_response
)
from .models import Photo
from sqlalchemy import asc, text
from . import db
import os
from werkzeug.utils import secure_filename
from PIL import Image # this imports the Pillow's image module

main = Blueprint('main', __name__)

# This is called when the home page is rendered. It fetches all images sorted by filename.
@main.route('/')
def homepage():
  photos = db.session.query(Photo).order_by(asc(Photo.file))
  return render_template('index.html', photos = photos)

@main.route('/uploads/<name>')
def display_file(name):
  return send_from_directory(current_app.config["UPLOAD_DIR"], name)

# Check if the extension is a supported file type
def allowed_image(filename):
  allowed_extensions = {'png', 'jpg', 'jpeg'}
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Verify that it is an image and not some other file with an image extension
def is_image(file):
  try:
    img = Image.open(file)
    img.verify() 
    return True
  except(IOError, SyntaxError) as e:
    print(f"File is not an image: {e}")
    return False
  
# Upload a new photo
@main.route('/upload/', methods=['GET','POST'])
def newPhoto():
  if request.method == 'POST':
    file = None
    if "fileToUpload" in request.files:
      file = request.files.get("fileToUpload")
    else:
      flash("Invalid request!", "error")

    if not file or not file.filename:
      flash("No file selected!", "error")
      return redirect(url_for('main.newPhoto'))
    
    if not allowed_image(file.filename):
      flash("File must be an Image file (png, jpg, jpeg)", "error")
      return redirect(url_for('main.newPhoto'))
    
    if not is_image(file):
      flash("File must be an Image file (png, jpg, jpeg)", "error")
      return redirect(url_for('main.newPhoto'))
    
    if file.tell() > 10485760:
      flash("File too large!", "error")
      return redirect(url_for('main.newPhoto'))

    filepath = os.path.abspath(os.path.join(current_app.config["UPLOAD_DIR"], secure_filename(file.filename)))
    file.save(filepath)

    newPhoto = Photo(name = request.form['user'], 
                    caption = request.form['caption'],
                    description = request.form['description'],
                    file = file.filename)
    db.session.add(newPhoto)
    flash('New Photo %s Successfully Created' % newPhoto.name)
    db.session.commit()
    return redirect(url_for('main.homepage'))
  else:
    return render_template('upload.html')

# This is called when clicking on Edit. Goes to the edit page.
@main.route('/photo/<int:photo_id>/edit/', methods = ['GET', 'POST'])
def editPhoto(photo_id):
  editedPhoto = db.session.query(Photo).filter_by(id = photo_id).one()
  if request.method == 'POST':
    if request.form['user']:
      editedPhoto.name = request.form['user']
      editedPhoto.caption = request.form['caption']
      editedPhoto.description = request.form['description']
      db.session.add(editedPhoto)
      db.session.commit()
      flash('Photo Successfully Edited %s' % editedPhoto.name)
      return redirect(url_for('main.homepage'))
  else:
    return render_template('edit.html', photo = editedPhoto)


# This is called when clicking on Delete. 
@main.route('/photo/<int:photo_id>/delete/', methods = ['GET','POST'])
def deletePhoto(photo_id):
  fileResults = db.session.execute(text('select file from photo where id = :photo_id'), {'photo_id': photo_id})
  filename = fileResults.first()[0]
  filepath = os.path.join(current_app.config["UPLOAD_DIR"], filename)
  os.unlink(filepath)
  db.session.execute(text('delete from photo where id = :photo_id'), {'photo_id': photo_id})
  db.session.commit()
  
  flash('Photo id %s Successfully Deleted' % photo_id)
  return redirect(url_for('main.homepage'))

