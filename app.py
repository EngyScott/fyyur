#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
from models import Venue, Artist, Shows, app, db
from flask_migrate import Migrate
from datetime import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
# app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
db.init_app(app)
# new_venue = Venue(name='Nano', city='Cairo', state='NA', address='120 orabi sydni', phone='2585265456', image_link='https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60', facebook_link='https://www.facebook.com/TheMusicalHop', website='', genres='Roll N Rock', seeking_talent=False, seeking_description='')

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

# -------------------------------------------------------------------
#  Venues
#  ----------------------------------------------------------------
# SHOW ALL 
# ===============
@app.route('/venues', )
def venues():
  # TODO: replace with real venues data.
  data = []
  venues = Venue.query.all()
  for place in Venue.query.distinct(Venue.city, Venue.state).all():
      data.append({
          'city': place.city,
          'state': place.state,
          'venues': [{
              'id': venue.id,
              'name': venue.name,
          } for venue in venues if
              venue.city == place.city and venue.state == place.state]
      })
  return render_template('pages/venues.html', areas=data)
# --------------------------------------------
# SEACHING VENUES
# ================
@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # GET VENUES MATCH THE SEARCH TERM
  data=[]
  search_term = request.form.get('search_term')
  venue_list = Venue.query.filter(Venue.name.ilike('%{}%'.format(search_term))).all()
  print(venue_list)
  
  for venue in venue_list:
    # build dic of id and name
    venue_data = {
      "id": venue.id,
      "name": venue.name,
    }
    # APPEND RETURED DATA TO DATA TO PASS
    data.append(venue_data)

  print(data)
  # ASSIGN DATA TO RESPONSE BE SENT TO FORM
  response={
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)
# --------------------------------
# SHOW ONE VENUE
# ==============
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data={}
  error = False
  try:
    # query upcoming shows with join artist and venue tables 
    upcoming_shows = db.session.query(Artist, Shows).join(Shows).join(Venue).\
      filter(
            Shows.venue_id == venue_id,
            Shows.start_time > datetime.now(),
            Shows.artist_id == Artist.id
          ).all()
    # print('upcoming_shows:', type(upcoming_shows), upcoming_shows)
    # query past Showss with join artist and venue tables 
    past_shows = db.session.query(Artist, Shows).join(Shows).join(Venue).\
      filter(
            Shows.venue_id == venue_id,
            Shows.start_time < datetime.now(),
            Shows.artist_id == Artist.id
      ).all()
    # print('past_shows:', type(past_shows), past_shows)
    
    # retrieve venue data from db
    venues = Venue.query.filter_by(id=venue_id).first_or_404()
    # print(venues)
    data = {
      'id': venues.id,
      'name': venues.name,
      'city': venues.city,
      'state': venues.state,
      'address': venues.address ,
      'phone': venues.phone,
      'facebook_link': venues.facebook_link,
      'genres': venues.genres,
      'website': venues.website,
      'image_link': venues.image_link,
      'seeking_talent': venues.seeking_talent,
      'seeking_description': venues.seeking_description,
      'upcoming_shows': [{
                        'artist_id': artist.id, 
                        'artist_name': artist.name, 
                        'start_time': show.start_time.strftime("%d-%m-%Y %H:%M"),
                        'artist_image_link': artist.image_link
                        } for artist, show in upcoming_shows],
      'past_shows' : [{
                        'artist_id': artist.id, 
                        'artist_name': artist.name, 
                        'start_time': show.start_time.strftime("%d-%m-%Y %H:%M"),
                        'artist_image_link': artist.image_link
                        }for artist, show in past_shows],
      'upcoming_shows_count' : len(upcoming_shows),
      'past_shows_count': len(past_shows)
    }
      # print('venues: ', venues)
  except:
    error = True
  finally:
    if error:
      abort(400)
    return render_template('pages/show_venue.html', venue=data)
# ------------------------
#  Create Venue
#  ============

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)
  error = False
  try:
    # TODO: insert form data as a new Venue record in the db, instead
    new_venue = Venue()
    form.populate_obj(new_venue)
    db.session.add(new_venue)
    db.session.commit()
      # on successful db insert, flash success
    flash('Venue %s is successfully created'%new_venue.name)
      # TODO: modify data to be the data object returned from db insertion
  except ValueError as e:
    print(e)
    error = True
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + new_venue.name + ' could not be listed.')
    db.session.rollback()
  finally:
    db.session.close()
    if error:
      abort(400)
    else:  
      error = False
      return redirect(url_for('index'))
  
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  
# -----------------------
# DELETE VENUE
# ============
@app.route('/venues/<venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  try:
    get_venue = Venue.query.get(venue_id)
    # print(get_venue)
    db.session.delete(get_venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    if error:
      flash('An error occurred. Venue ' + get_venue.name + ' could not be deleted, try again later.')
    else:
      db.session.close()
      return redirect(url_for('index'))
  
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
# -----------------------------------------------------------------
#  Artists
#  ----------------------------------------------------------------
# SHOW ALL
# ========
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=[]
  try:
    all_artists = Artist.query.all()
    for artist in all_artists:
      one = {'id' : artist.id, "name" : artist.name}
      data.append(one)
    # print('data:', data)
  except:
    abort(400)
  finally:
    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  data=[]
  search_term = request.form.get('search_term')
  # find all matched artist names
  artist_list = Artist.query.filter(Artist.name.ilike('%{}%'.format(search_term))).all()
  # print(artist_list)
  # build dic of name & id
  for artist in artist_list:
    artist_data = {
      "id": artist.id,
      "name": artist.name,
    }
    # APPEND RETURED DATA TO DATA TO PASS
    data.append(artist_data)

  # print(data)
  # ASSIGN DATA TO RESPONSE BE SENT TO FORM
  response={
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

# -------------------------------------------------------------------------------------------
# SHOW ONE ARTIST
# ===============
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  try:
    # query upcoming shows with join artist and venue tables 
    upcoming_shows = db.session.query(Venue, Shows).join(Shows).join(Artist).\
      filter(
              Shows.artist_id == artist_id,
              Shows.start_time > datetime.now(),
              Shows.venue_id == Venue.id
            ).all()
    # print('upcoming_shows:', type(upcoming_shows), upcoming_shows)
    # query past Showss with join artist and venue tables 
    past_shows = db.session.query(Venue,Shows).join(Shows).join(Artist).\
      filter(
        Shows.artist_id == artist_id,
        Shows.start_time < datetime.now(),
        Shows.venue_id == Venue.id
      ).all()
    # print('past_shows:', type(past_shows), past_shows)
    # retrieve artist data from db
    artists = Artist.query.filter_by(id=artist_id).first_or_404()
    # print('artists:', artists)
    data ={
      'id' : artists.id,
      'name': artists.name,
      'city' : artists.city,
      'state' : artists.state,
      'phone' : artists.phone,
      'facebook_link' : artists.facebook_link,
      'genres' : artists.genres,
      'website' : artists.website,
      'image_link' : artists.image_link,
      'seeking_venue' : artists.seeking_venue,
      'seeking_description' : artists.seeking_description,
      'upcoming_shows': [{
                        'venue_id': venue.id,
                        'venue_name': venue.name,
                        'start_time': show.start_time.strftime("%d-%m-%Y %H:%M"), 
                        'venue_image_link': venue.image_link
                        }for show, venue in upcoming_shows],
      'past_shows': [{
                        'venue_id': venue.id, 
                        'venue_name': venue.name, 
                        'start_time': show.start_time.strftime("%d-%m-%Y %H:%M"), 
                        'venue_image_link': venue.image_link
                      }for show, venue in past_shows],
      'past_shows_count': len(past_shows),
      'upcoming_shows_count' : len(upcoming_shows)
    }
  except:
    abort(400)
  finally:
    return render_template('pages/show_artist.html', artist=data)
#  ----------------------------------------------------------------
#  Update ARTIST
# ==============
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # TODO: populate form with fields from artist with ID <artist_id>
    # fill form fields with artist data 
  artist = Artist.query.get(artist_id)
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres
  form.facebook_link.data = artist.facebook_link
  form.website.data = artist.website
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  try:
    # artist record with ID <artist_id> using the new attributes
    artist = Artist.query.get(artist_id)
    # update fields
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.genres = request.form['genres']
    artist.facebook_link = request.form['facebook_link']
    # update the db
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))
#  ----------------------------------------------------------------
#  Update VENUES
# ==============
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  # fill form fields with venue data 
  venue = Venue.query.get(venue_id)
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.phone.data = venue.phone
  form.genres.data = venue.genres
  form.facebook_link.data = venue.facebook_link
  form.address.data = venue.address
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  try:
    # venue record with ID <venue_id> using the new attributes
    venue = Venue.query.get(venue_id)
    # update fields
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.phone = request.form['phone']
    venue.genres = request.form['genres']
    venue.facebook_link = request.form['facebook_link']
    venue.address = request.form['address']
    # update the db
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))
#  ----------------------------------------------------------------
#  Create Artist
# ===============

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)
  # called upon submitting the new artist listing form
  # fetch data from form
  error=False
  try:
    # TODO: insert form data as a new Artist record in the db
    new_artist = Artist()
    form.populate_obj(new_artist)
    # print('new_artist:', new_artist)
    db.session.add(new_artist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist %s was successfully listed!'%new_artist.name)
    # TODO: modify data to be the data object returned from db insertion
  except:
    error=True
    db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist %s could not be listed.'%form.name)
  finally:
    db.session.close()
    if error:
      abort(400)
      # return jsonify(data)
    return redirect(url_for('index'))
# ----------------------------------------------------------------------
#  Shows
#  ---------------------------------------------------------------------
# SHOW ALL
# ========
@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[]
  try:
    all_shows = Shows.query.all()
    for show in all_shows:
      # print(show)
      one = {
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time
      }
      # print(one)
      data.append(one)
      # print('data:', data)
  except:
    abort(400)
  finally:
    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # collect the information from the form
  start_time = request.form['start_time']
  venue_id = request.form['venue_id']
  artist_id = request.form['artist_id']
  # data = []
  error = False
  # TODO: insert form data as a new Show record in the db, instead
  try:
    # assign the information for a new show record
    new_show = Shows(start_time=start_time, venue_id=venue_id, artist_id=artist_id)
    # print(new_show)
    # inject information to the db
    db.session.add(new_show)
    db.session.commit()
    # retrieve back the information
    # created_show_id = new_show.id
    # data['start_time'] = new_show.start_time
    # data['venue_id'] = new_show.venue_id
    # data['artist_id'] = new_show.artist_id
  except:
    error = True
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Show could not be listed.')
    db.session.rollback()
  finally:
    db.session.close()
    if error:
      abort(400)
    else:
      # on successful db insert, flash success
      flash('Show was successfully listed!')
      # return jsonify(data) 
      return redirect(url_for('index'))
  
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# db.create_all()
# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
