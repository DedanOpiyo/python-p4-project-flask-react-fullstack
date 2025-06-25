from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from flask_sqlalchemy import SQLAlchemy # Remove func
from sqlalchemy import func # Import from sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates

# metadata = MetaData(
#     naming_convention={
#         "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#     }
# )

# db = SQLAlchemy(metadata=metadata)

from config import db

# Models go here!
class Service(db.Model, SerializerMixin):
    __tablename__='services'
    
    id = db.Column(db.Integer, primary_key=True)
    service_type = db.Column(db.String)

    service_fundis = db.relationship('Fundi', back_populates='service')

    # Serializer rules
    serialize_rules = ('-service_fundis.service', )

class County(db.Model, SerializerMixin):
    __tablename__='counties'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    county_fundis = db.relationship('Fundi', back_populates='county')

    # Serializer rules
    serialize_rules = ('-county_fundis.county', )
  
class Fundi(db.Model, SerializerMixin):
    __tablename__='fundis'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    phonenumber = db.Column(db.String) # db.Float may lose 0, at the beginning
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    county_id = db.Column(db.Integer, db.ForeignKey('counties.id'))

    service = db.relationship('Service', back_populates='service_fundis')
    county = db.relationship('County', back_populates='county_fundis')
    fundi_bookings = db.relationship('Booking', back_populates='fundi')

    # Serializer rules
    serialize_rules = ('-service.service_fundis', '-county.county_fundis', )
 

class User(db.Model, SerializerMixin):

    __tablename__='users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String) # db.Integer may lose starting 0. faker.phone_number() uses string
    password_hash = db.Column(db.String, nullable=False)

    user_bookings = db.relationship('Booking', back_populates='user')

    # Serializer rules
    serialize_rules = ('-user_bookings.user', )

class Booking(db.Model, SerializerMixin):
    __tablename__='bookings'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(), server_default= func.now())
    updated_at = db.Column(db.DateTime(), onupdate=func.now())

    fundi_id = db.Column(db.Integer, db.ForeignKey('fundis.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates='user_bookings')
    fundi = db.relationship('Fundi', back_populates='fundi_bookings')
    reviews = db.relationship('Review', back_populates='review_booking') # Many revies for booking | Single review per booking?

    # Serializer rules
    serialize_rules = ('-user.user_bookings', '-fundi.fundi_bookings', '-reviews.review_booking', )

class Review(db.Model, SerializerMixin):
    __tablename__='reviews' # fix __tablename___

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    created_at = db.Column(db.DateTime(), server_default= func.now())
    updated_at = db.Column(db.DateTime(), onupdate=func.now())

    
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id')) # If we want one review per booking: Add unique=True (then adjust relationship to singular i.e back_populates='review')

    review_booking = db.relationship('Booking', back_populates='reviews') # Or review

    # Serializer rules
    serialize_rules = ('-review_booking.reviews', )
  

#     fundi_id = db.Column(db.Integer, db.ForeignKey('fundis.id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# class Admin(db.Model, SerializerMixin):
#     __tablename__='admins'

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String)
#     email = db.Column(db.String(100), nullable=False, unique=True)
#     password_hash = db.Column(db.String, nullable=False)






