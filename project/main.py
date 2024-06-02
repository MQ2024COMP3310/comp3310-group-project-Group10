import imghdr
from unittest import loader
from flask import (
  Blueprint, render_template, request, 
  flash, redirect, url_for, send_from_directory, 
  current_app, make_response
)
from flask_login import current_user, login_required
from .models import Photo, User
from sqlalchemy import asc, text
from . import db
import os
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)
supported_filetypes = ['png', 'jpg', 'jpeg']

# This is called when the home page is rendered. It fetches all images sorted by filename.
@main.route('/')
def homepage():
  # Feature 3/4 from spec implementation (edited)
  photos = db.session.query(Photo).filter_by(public = True).filter_by(category = None).order_by(asc(Photo.file))
  return render_template('index.html', photos = photos)

@main.route('/uploads/<name>')
def display_file(name):
  return send_from_directory(current_app.config["UPLOAD_DIR"], name)

def allowed_image(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in supported_filetypes

# Upload a new photo
@main.route('/upload/', methods=['GET','POST'])
@login_required #prevents users without accounts from uploading photos
def newPhoto():
  if request.method == 'POST':
    file = None
    if "fileToUpload" in request.files:
      file = request.files.get("fileToUpload")
    else:
      flash("Invalid request!", "error")

    if not file or not file.filename:
      flash("No file selected!", "error")
      return redirect(url_for('main.homepage')) # using in application redirection to prevent open redirect attacks

    # checks file extension to make sure it's of a supported type
    if not allowed_image(file.filename):
      flash("File must be an Image file (png, jpg, jpeg)", "error")
      return redirect(url_for('main.newPhoto'))
    
    # use built in python library to reduce 3rd party dependencies
    # checks the file metadata and cross references to supported filetypes
    # to ensure the uploaded image is an image file and not any other file
    # with the extension changed.
    if imghdr.what(file) not in supported_filetypes:
      flash("File must be an Image file (png, jpg, jpeg)", "error")
      return redirect(url_for('main.newPhoto'))
    
    # uses the tell() method to check size of file and makes sure it isn't
    # larger than 10MB (HD photos are 5-10MB on average)
    if file.tell() > 10485760:
      flash("File too large!", "error")
      return redirect(url_for('main.newPhoto'))

    filepath = os.path.join(current_app.config["UPLOAD_DIR"], secure_filename(file.filename)) # used secure_filename to prevent path traversal attacks by sanitising file names
    file.save(filepath)

    newPhoto = Photo(name = request.form['user'], 
                    caption = request.form['caption'],
                    description = request.form['description'],
                    public = True if request.form['public'] == 'publicOpt' else False, # Feature 4 from spec implementation
                    category = None if request.form['category'] == 'default' else request.form['category'], # Feature 3 from spec implementation
                    file = file.filename)
    db.session.add(newPhoto)
    flash('New Photo %s Successfully Created' % newPhoto.name)
    db.session.commit()
    return redirect(url_for('main.homepage'))
  else:
    return render_template('upload.html')

# This is called when clicking on Edit. Goes to the edit page.
@main.route('/photo/<int:photo_id>/edit/', methods = ['GET', 'POST'])
@login_required #prevents users without accounts from editing photos
def editPhoto(photo_id):
  editedPhoto = db.session.query(Photo).filter_by(id = photo_id).one()
  if(editedPhoto.user_id == current_user.id or current_user.is_admin): #checks if user is publisher of photo
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
      return render_template('edit.html', photo = editedPhoto) #allows editing if publisher
  else:
    flash('You do not have permission to edit this photo!')
    return redirect(url_for('main.homepage')) #reloads homepage if not the publisher


# This is called when clicking on Delete. 
@main.route('/photo/<int:photo_id>/delete/', methods = ['GET','POST'])
@login_required #prevents users without accounts from deleting photos
def deletePhoto(photo_id):
  photoToDelete = db.session.query(Photo).filter_by(id = photo_id).one() #allows you to call photos variables
  if(photoToDelete.user_id == current_user.id or current_user.is_admin): #checks if user is publisher of photo
    fileResults = db.session.execute(text('select file from photo where id = :photo_id'), {'photo_id': photo_id}) # parameterised queries to prevent SQL injection
    filename = fileResults.first()[0]
    filepath = os.path.join(current_app.config["UPLOAD_DIR"], filename)
    os.unlink(filepath)
    db.session.execute(text('delete from photo where id = :photo_id'), {'photo_id': photo_id}) # parameterised queries to prevent SQL injection
    db.session.commit()
  
    flash('Photo id %s Successfully Deleted' % photo_id)
    return redirect(url_for('main.homepage')) #deletes image if publisher
  else:
    flash('You do not have permission to delete this photo!')
    return redirect(url_for('main.homepage')) #reloads homepage if not the publisher
  
# This is called when directly navigating to the photo page.
@main.route('/photo/<int:photo_id>/')
def viewPhoto(photo_id):
  photo = db.session.query(Photo).filter_by(id = photo_id).one()
  return render_template('view.html', photo = photo)

# Feature 3 from spec implementation
@main.route('/<string:category>/')
def category(category):
  photos = db.session.query(Photo).filter_by(public = True).filter_by(category = category).order_by(asc(Photo.file))
  return render_template('index.html', photos = photos) 