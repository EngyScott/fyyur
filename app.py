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
from flask_wtf import Form
from forms import *
from config import app, db
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

moment = Moment(app)
app.config.from_object('config')
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
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class Venue(db.Model):
  __tablename__ = 'venue'
  id = db.Column(db.Integer,db.Sequence('venue_seq'), primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  address = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  website = db.Column(db.String())
  genres = db.Column(db.String())
  seeking_talent = db.Column(db.Boolean, default=False)
  seeking_description = db.Column(db.String())
  shows = db.relationship('Shows', lazy=True, backref='venue')

  def __repr__(self):
    return f'<{self.id}, {self.name}, {self.city}, {self.state}, {self.address}, {self.phone}, {self.image_link}, {self.facebook_link}, {self.genres}, {self.seeking_talent}, {self.seeking_description}>'
    
    # DONE: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
  __tablename__ = 'artist'
  id = db.Column(db.Integer,db.Sequence('artist_seq'), primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.String())
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  website = db.Column(db.String())
  seeking_venue = db.Column(db.Boolean, default=False)
  seeking_description = db.Column(db.String())
  shows = db.relationship('Shows', lazy=True, backref='artist')
  def __repr__(self):
    return f'<{self.id}, {self.name}, {self.city}, {self.state}, {self.phone}, {self.genres}, {self.image_link}, {self.facebook_link}, {self.seeking_venue}, {self.seeking_description}>'

    # DONE: implement any missing fields, as a database migration using Flask-Migrate

# DONE Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
#     
class Shows(db.Model):
  __tablename__ = 'shows'
  id = db.Column(db.Integer,db.Sequence('show_seq'),primary_key=True)
  start_time = db.Column(db.DateTime, nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
  def __repr__(self):
    return f'<{self.id}, {self.start_time}, {self.venue_id}, {self.artist_id}>'

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
  # try:
  all_venues = Venue.query.all()
  venues=[]
  today = datetime.now()
  item = {}
  for venue in all_venues:
    # print("venue.city: ", venue.city)
    item['city'] = venue.city
    item['state'] = venue.state
    # item['venues']
    # item['venues']
    num_upcoming_shows = 0
    shows = Shows.query.filter(Shows.venue_id == venue.id).all()
    # print(shows)
    for show in shows:
      if show.start_time > today:
        num_upcoming_shows +=1
    print('num_upcoming_shows :', num_upcoming_shows)
      # num_upcoming_shows+=1
    # print(num_upcoming_shows)

    # upcoming_shows = shows.filter_by(int(start_time) > int(datetime.now()))
    # num_upcoming_shows = upcoming_shows.count()
    # print('upcoming_shows:', upcoming_shows)
    # num_upcoming_shows = upcoming_shows.count()
    # print(venue.id)
    venues.append({
                  "id": venue.id,
                  "name": venue.name,
                  "num_upcoming_shows": num_upcoming_shows
                })
  # except:
  #   pass
  # finally:
  #   pass
  
  data=[{
    "city": "San Francisco",
    "state": "CA",
    "venues": [{
      "id": 1,
      "name": "The Musical Hop",
      "num_upcoming_shows": 0,
    }, {
      "id": 3,
      "name": "Park Square Live Music & Coffee",
      "num_upcoming_shows": 1,
    }]
  }, {
    "city": "New York",
    "state": "NY",
    "venues": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }]
  return render_template('pages/venues.html', areas=data);
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
  # data1={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #   "past_shows": [{
  #     "artist_id": 4,
  #     "artist_name": "Guns N Petals",
  #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  data = {}
  upcoming_shows_count = 0
  past_shows_count = 0
  past_shows = []
  upcoming_shows = []
  today = datetime.now()
  items = {}
  try:
    # retrieve venue data from db
    get_venue = Venue.query.get(venue_id)
    # print(get_venue)
    # get shows of venue
    shows = Shows.query.filter(Shows.venue_id == get_venue.id).all()
    # print('shows:', shows)
    for show in shows:
      items['start_time'] = show.start_time
      artists = Artist.query.filter(show.artist_id == Artist.id).all()
      # print(artists)
      for artist in artists:
        items['artist_id'] = artist.id
        items['artist_name'] = artist.name
        items['artist_image_link'] = artist.image_link
        print(items)
        if int(show.start_time) > int(today):
          upcoming_shows_count +=1
          upcoming_shows.append(items)
        else:
          past_shows_count += 1
          past_shows.append(items)
    print('upcoming_shows_count: '+ upcoming_shows_count)
    print('past_shows_count:'+ past_shows_count)
    print('past_shows:'+ past_shows)
    print('upcoming_shows:'+ upcoming_shows)
    data = {
      'name': get_venue.name,
      'id': get_venue.id,
      'city': get_venue.city,
      'state': get_venue.state,
      'address': get_venue.address ,
      'phone': get_venue.phone,
      'facebook_link': get_venue.facebook_link,
      'genres': get_venue.genres,
      'website': get_venue.website,
      'image_link': get_venue.image_link,
      'seeking_talent': get_venue.seeking_talent,
      'seeking_description': get_venue.seeking_description,
      'upcoming_shows_count': upcoming_shows_count,
      'past_shows_count': past_shows_count,
      'past_shows': past_shows,
      'upcoming_shows': upcoming_shows
    }
    print('data: '+ data)
  except Expression as e:
    print(e)
  finally:
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
  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  address = request.form['address']
  phone = request.form['phone']
  facebook_link = request.form['facebook_link']
  data = {}
  error = False
  try:
    print(name, city, state, address, phone, facebook_link)
    # TODO: insert form data as a new Venue record in the db, instead
    max_id = db.session.query(db.func.max(Venue.id)).scalar()
    users = db.session.query(User).filter(User.numLogins == max_logins).all()
    new_venue = Venue(name=name, city=city, state=state, 
                      address=address, phone=phone,
                      facebook_link=facebook_link)
    db.session.add(new_venue)
    db.session.commit()
      # TODO: modify data to be the data object returned from db insertion
    created_venue = new_venue.id
    print('created_venue:', created_venue)
    data['id'] = new_venue.id
    data['name'] = new_venue.name
    data['city'] = new_venue.city
    data['state'] = new_venue.state
    data['address'] = new_venue.address 
    data['phone'] = new_venue.phone
    data['facebook_link'] = new_venue.facebook_link
    print('data:', data)
  except Exception as e:
    print(e)
    error = True
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    db.session.rollback()
  finally:
    if error:
      abort(400)
    else:  
      error = False
      db.session.close()
      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
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
    print(get_venue)
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
  data=[{
    "id": 4,
    "name": "Guns N Petals",
  }, {
    "id": 5,
    "name": "Matt Quevedo",
  }, {
    "id": 6,
    "name": "The Wild Sax Band",
  }]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  data=[]
  search_term = request.form.get('search_term')
  # find all matched artist names
  artist_list = Artist.query.filter(Artist.name.ilike('%{}%'.format(search_term))).all()
  print(artist_list)
  # build dic of name & id
  for artist in artist_list:
    artist_data = {
      "id": artist.id,
      "name": artist.name,
    }
    # APPEND RETURED DATA TO DATA TO PASS
    data.append(artist_data)

  print(data)
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
  # data1={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "past_shows": [{
  #     "venue_id": 1,
  #     "venue_name": "The Musical Hop",
  #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  artist = {}
  error = False
  get_artist = Artist.query.get(artist_id)
  print('get_artist:', get_artist)
  try:
    artist['name'] = get_artist.name
    artist['id'] = get_artist.id
    artist['city'] = get_artist.city
    artist['state'] = get_artist.state
    artist['phone'] = get_artist.phone
    artist['facebook_link'] = get_artist.facebook_link
    artist['genres'] = list(get_artist.genres)
    artist['website'] = get_artist.website
    artist['image_link'] = get_artist.image_link
    artist['seeking_venue'] = get_artist.seeking_venue
    artist['seeking_description'] = get_artist.seeking_description
    print('data:', artist)
  except Expression as e:
    print(e)
    error= True
  finally:
    if error:
      flash('Artist with id '+ artist_id + 'is not found')
    else:
      return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
    # fill form fields with artist data 
  artist = Artist.query.get(artist_id)
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres
  form.facebook_link.data = artist.facebook_link
  # TODO: populate form with fields from artist with ID <artist_id>
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

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  phone = request.form['phone']
  genres = request.form['genres']
  facebook_link = request.form['facebook_link']

  data = {}
  error = False
  if name is None:
    error = True
    abort(400)
  else:
      error=False
      try:
        # TODO: insert form data as a new Artist record in the db
        new_artist = Artist(name=name, city=city, state=state, \
                            phone=phone, genres=genres, \
                            facebook_link=facebook_link)
        print('new_artist:', new_artist)
        db.session.add(new_artist)
        db.session.commit()
          # TODO: modify data to be the data object returned from db insertion
        created_artist = new_artist.id
        print('created_artised: ', created_artist)
        data['id']=new_artist.id
        data['name']=new_artist.name
        data['city']=new_artist.city
        data['state']=new_artist.state
        data['phone']=new_artist.phone
        data['genres']=new_artist.genres
        data['facebook_link']=new_artist.facebook_link
        print('data: ', data)
      except:
        error=True
        db.session.rollback()
        # TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Artist ' + data['name'] + ' could not be listed.')
      finally:
        db.session.close()
        if error:
          abort(400)
        else:
          # on successful db insert, flash success
          flash('Artist ' + request.form['name'] + ' was successfully listed!')
          error=False
          # return jsonify(data)
          return redirect(url_for('index'))

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]
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
  error = False
  # TODO: insert form data as a new Show record in the db, instead
  try:
    # assign the information for a new show record
    new_show = Shows(start_time=start_time, venue_id=venue_id, artist_id=artist_id)
    print(new_show)
    # inject information to the db
    db.session.add(new_show)
    db.session.commit()
    # retrieve back the information
    created_show_id = new_show.id
    data['start_time'] = new_show.start_time
    data['venue_id'] = new_show.venue_id
    data['artist_id'] = new_show.artist_id
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
