# main.py
from config import *

# Your main application logic goes here



class Space(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    space_name = db.Column(db.String(255), nullable=False)
    space_description = db.Column(db.String(255), nullable=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(255), nullable=False)
    space_id = db.Column(db.Integer, db.ForeignKey('space.id'), nullable=False)

class Subcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subcategory_name = db.Column(db.String(255), nullable=False)
    parent_subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'))
    parent_subcategory_name = db.Column(db.String(255), db.ForeignKey('subcategory.subcategory_name'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category_name = db.Column(db.String(255), db.ForeignKey('category.category_name'))

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), nullable=False)
    image = db.Column(db.LargeBinary, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category_name = db.Column(db.String(255), db.ForeignKey('category.category_name'))
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=False)
    subcategory_name = db.Column(db.String(255), db.ForeignKey('subcategory.subcategory_name'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()