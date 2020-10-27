from app import db

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class Venue(db.Model):
  __tablename__ = 'venue'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  address = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  website = db.Column(db.String())
  genres = db.Column(db.ARRAY(db.String()))
  seeking_talent = db.Column(db.Boolean, default=False)
  seeking_description = db.Column(db.String())
  shows = db.relationship('Shows', lazy=True, backref='venue')

  def __repr__(self):
    return f'<{self.id}, {self.name}, {self.city}, {self.state}, {self.address}, {self.phone}, {self.image_link}, {self.facebook_link}, {self.genres}, {self.seeking_talent}, {self.seeking_description}>'
    
    # DONE: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
  __tablename__ = 'artist'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.ARRAY(db.String()))
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
