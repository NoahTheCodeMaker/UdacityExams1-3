# Imports

import traceback
import dateutil.parser
import babel
import logging
import collections
import collections.abc
from forms import *
from datetime import datetime
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler
from flask import Flask, render_template, request, flash, redirect, url_for, abort
collections.Callable = collections.abc.Callable

# App Config.

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/fyurr'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.create_all()

# Models

from models import *

# Filters.

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

# Functions

def count_past_shows(shows):
  past_shows_count = 0
  for show in shows:
    if show.time < datetime.today():
      past_shows_count += 1
  return(past_shows_count)

def count_upcoming_shows(shows):
  upcoming_shows_count = 0
  for show in shows:
    if show.time >= datetime.today():
      upcoming_shows_count += 1
  return(upcoming_shows_count)

def past_shows_decorator(shows):
  data = []
  for show in shows:
    if show.time < datetime.today():
      artist = Artist.query.get(show.artist_id)
      venue = Venue.query.get(show.venue_id)
      data.append({
        "artist_id": show.artist_id,
        "venue_id": show.venue_id,
        "artist_name": artist.name,
        "venue_name": venue.name,
        "artist_image_link": artist.image_link,
        "venue_image_link": venue.image_link,
        "start_time": str(show.time)
      })
  return data

def upcoming_shows_decorator(shows):
  data = []
  for show in shows:
    if show.time >= datetime.today():
      artist = Artist.query.get(show.artist_id)
      venue = Venue.query.get(show.venue_id)
      data.append({
        "artist_id": show.artist_id,
        "venue_id": show.venue_id,
        "artist_name": artist.name,
        "venue_name": venue.name,
        "artist_image_link": artist.image_link,
        "venue_image_link": venue.image_link,
        "start_time": str(show.time)
      })
  return data

# Controllers.

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  # venues = Venue.query.all()
  # data = []
  # areas = Venue.query.group_by
  # for venue in venues:

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
  return render_template('pages/venues.html', areas=data)

# Venue Search Route Handler
@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

# Views Venues by their ID
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  shows_at_venue = Show.query.filter_by(venue_id=venue_id).all()
  venue = Venue.query.get(venue_id)
  data={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows_decorator(shows_at_venue),
    "upcoming_shows": upcoming_shows_decorator(shows_at_venue),
    "past_shows_count": count_past_shows(shows_at_venue),
    "upcoming_shows_count": count_upcoming_shows(shows_at_venue)
  }
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form, meta={'crsf': False})
  if form.validate():
    error = False
    data = {}
    try:
      newVenue = Venue(
        name=form.name.data, 
        city=form.city.data, 
        state=form.state.data,
        address=form.address.data, 
        phone=form.phone.data, 
        image_link=form.image_link.data, 
        facebook_link=form.facebook_link.data,
        genres=form.genres.data, 
        website_link=form.website_link.data,
        seeking_talent=form.seeking_talent.data, 
        seeking_description=form.seeking_description.data
      )
      db.session.add(newVenue)
      db.session.commit()
      data = newVenue
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
      error = True
      db.session.rollback()
      traceback.print_exc()
    finally:
      db.session.close()
      if error == True:
            abort(400)
  else:
    message = []
    for field, err in form.errors.items():
        message.append(field + ' ' + '|'.join(err))
    flash('Something Went Wrong! - ' + str(message))

  return render_template('pages/home.html', data=data)

# Delete Venue
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('pages/home.html'))

#  Artists

@app.route('/artists')
def artists():
  data = Artist.query.order_by(Artist.id).all()
  return render_template('pages/artists.html', artists=data)

# Artist Search Handler
@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  results = Artist.query.filter(Artist.name.ilike("%{}%".format(search_term))).all()
  response={
    "count": len(results),
    "data": results
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

# Views Artists by their ID
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  shows_performed = Show.query.filter_by(artist_id=artist_id).all()
  data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows_decorator(shows_performed),
    "upcoming_shows": upcoming_shows_decorator(shows_performed),
    "past_shows_count": count_past_shows(shows_performed),
    "upcoming_shows_count": count_upcoming_shows(shows_performed)
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update Artists and Venues

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  form.state.data = artist.state
  form.genres.data = artist.genres
  form.seeking_venue.data = artist.seeking_venue
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm(request.form, meta={'crsf': False})
  if form.validate():
    try:
      artist = Artist.query.get(artist_id)
      artist.name = form.name.data
      artist.city = form.city.data
      artist.state = form.state.data
      artist.phone = form.phone.data
      artist.image_link = form.image_link.data
      artist.facebook_link = form.facebook_link.data
      artist.genres = form.genres.data
      artist.website_link = form.website_link.data
      artist.seeking_venue = form.seeking_venue.data
      artist.seeking_description = form.seeking_description.data
      db.session.commit()
    except:
      db.session.rollback()
      traceback.print_exc()
    finally:
      db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  form.state.data = venue.state
  form.genres.data = venue.genres
  form.seeking_talent.data = venue.seeking_talent
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm(request.form, meta={'crsf': False})
  if form.validate():
    try:
      venue = Venue.query.get(venue_id)
      venue.name = form.name.data
      venue.city = form.city.data
      venue.state = form.state.data
      venue.address = form.address.data
      venue.phone = form.phone.data
      venue.image_link = form.image_link.data
      venue.facebook_link = form.facebook_link.data
      venue.genres = form.genres.data
      venue.website_link = form.website_link.data
      venue.seeking_talent = form.seeking_talent.data
      venue.seeking_description = form.seeking_description.data
      db.session.commit()
    except:
      db.session.rollback()
      traceback.print_exc()
    finally:
      db.session.close()
      
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form, meta={'crsf': False})
  if form.validate():
    data = {}
    error = False
    try:
      new_artist = Artist(
        name=form.name.data, 
        city=form.city.data, 
        state=form.state.data, 
        phone=form.phone.data, 
        image_link=form.image_link.data, 
        facebook_link=form.facebook_link.data, 
        genres=form.genres.data, 
        website_link=form.website_link.data, 
        seeking_venue=form.seeking_venue.data, 
        seeking_description=form.seeking_description.data
      )
      db.session.add(new_artist)
      db.session.commit()
      data = new_artist
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
      error = True
      db.session.rollback()
      traceback.print_exc()
    finally:
      db.session.close()
      if error == True:
            abort(400)
  else:
    message = []
    for field, err in form.errors.items():
        message.append(field + ' ' + '|'.join(err))
    flash('Something Went Wrong! - ' + str(message))

  return render_template('pages/home.html', data=data)

#  Shows

# Route handler for show browsing
@app.route('/shows')
def shows():
  shows = Show.query.all()
  data = []
  for show in shows:
    venue = Venue.query.get(show.venue_id)
    artist = Artist.query.get(show.artist_id)
    data.append({
      "venue_id": show.venue_id,
      "venue_name": venue.name,
      "artist_id": show.artist_id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": str(show.time)
      })
  return render_template('pages/shows.html', shows=data)

# Renders form
@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

# Route handler for Show creation
@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm(request.form, meta={'crsf': False})
  if form.validate():
    error = False
    data = {}
    try:
      new_show = Show(
        artist_id=form.artist_id.data, 
        venue_id=form.venue_id.data, 
        time=form.start_time.data
      )
      db.session.add(new_show)
      db.session.commit()
      data = new_show
      flash('Show was successfully listed!')
    except:
      error = True
      db.session.rollback()
      traceback.print_exc()
    finally:
      db.session.close()
      if error == True:
        abort(400)
  else:
    message = []
    for field, err in form.errors.items():
        message.append(field + ' ' + '|'.join(err))
    flash('Something Went Wrong! - ' + str(message))
  return render_template('pages/home.html', data=data)

# 404 Not Found Error
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

# 500 Level is Server Error
@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

# Settings
if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# Launch on Default port:
if __name__ == '__main__':
    app.run()