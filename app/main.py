from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    
    reviews = relationship('Review', back_populates='restaurant')

    def customers(self):
        return [review.customer for review in self.reviews]

    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(cls.price.desc()).first()

    def all_reviews(self):
        return [review.full_review() for review in self.reviews]

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    reviews = relationship('Review', back_populates='customer')

    def restaurants(self):
        return [review.restaurant for review in self.reviews]

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        rated_restaurants = [review.restaurant for review in self.reviews]
        return max(rated_restaurants, key=lambda r: r.average_rating())

    def add_review(self, restaurant, rating):
        new_review = Review(customer=self, restaurant=restaurant, rating=rating)
        session.add(new_review)
        session.commit()

    def delete_reviews(self, restaurant):
        reviews_to_delete = [review for review in self.reviews if review.restaurant == restaurant]
        for review in reviews_to_delete:
            session.delete(review)
        session.commit()

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    rating = Column(Integer)

    customer = relationship('Customer', back_populates='reviews')
    restaurant = relationship('Restaurant', back_populates='reviews')

    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.rating} stars."

    def __repr__(self):
        return f"<Review(customer={self.customer.full_name()}, restaurant={self.restaurant.name}, rating={self.rating})>"

# Create an SQLite database in memory for testing
engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()