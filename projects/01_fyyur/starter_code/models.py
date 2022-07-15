# 1NF - Single Valued Cells, Entries in column are same type, Rows are Unique
# 2NF - All attributes dependent on the key
# 3NF - All fields can be determined Only by the Key in the table and no other column
# 4NF - No multi-valued dependencies except on the key 
# 5NF - Cannot describe the table as being the logical result of joining other tables together

from app import db

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.Array(db.String), nullable=False)
    website_link = db.Column(db.String(120), nullable=True)
    seeking_talent = db.column(db.Boolean, nullable=True)
    seeking_description = db.column(db.String, nullable=False)

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.Array(db.String), nullable=False)
    website_link = db.Column(db.String(120), nullable=True)
    seeking_venue = db.column(db.Boolean, nullable=True)
    seeking_description = db.column(db.String, nullable=False)

Show = db.Table(
    "show",
    db.Column('id', db.Integer, primary_key=True),
    db.Column('time', db.DateTime, nullable=False),
    db.Column('venue_id', db.Integer, db.ForeignKey('venue.id')),
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'))
)