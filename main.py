from models import *

# space
class SpaceResource(Resource):
    def get(self, space_name=None):
        if space_name:
            space = Space.query.filter_by(space_name=space_name).first()
            if space:
                return [{'id': space.id, 'space_name': space.space_name, 'space_description': space.space_description}]
            else:
                return {'message': 'Space not found'}, 404
        else:
            spaces = Space.query.all()
            return [{'id': space.id, 'space_name': space.space_name, 'space_description': space.space_description} for space in spaces]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('space_name', type=str, required=True)
        parser.add_argument('space_description', type=str, required=False)
        args = parser.parse_args()
        space = Space(space_name=args['space_name'], space_description=args['space_description'])
        db.session.add(space)
        db.session.commit()
        return {'id': space.id, 'space_name': space.space_name, 'space_description': space.space_description}

#category
class CategoryResource(Resource):
    def get(self, space_name=None):
        if space_name:
            space = Space.query.filter_by(space_name=space_name).first()
            if space:
                categories = Category.query.filter_by(space_id=space.id).all()
                return jsonify([{'id': category.id, 'category_name': category.category_name, 'space_id': category.space_id} for category in categories])
            else:
                return jsonify({'message': 'Space not found'}), 404
        else:
            categories = Category.query.all()
            return jsonify([{'id': category.id, 'category_name': category.category_name, 'space_id': category.space_id} for category in categories])
    def post(self, space_name):
        parser = reqparse.RequestParser()
        parser.add_argument('category_name', type=str, required=True)
        args = parser.parse_args()
        space = Space.query.filter_by(space_name=space_name).first()
        if space:
            category = Category(category_name=args['category_name'], space_id=space.id)
            db.session.add(category)
            db.session.commit()
            return jsonify({'id': category.id, 'category_name': category.category_name, 'space_id': category.space_id})
        else:
            return jsonify({'error': 'Space not found'}), 404
#subcategory
class SubcategoryResource(Resource):
    def get(self,space_name=None ,category_name=None, parent_subcategory_name=None):
        if space_name:
            space = space.query.filter_by(space_name=space_name).first()
            if space:
                if category_name:
                    category = Category.query.filter_by(category_name=category_name).first()
                    if category:
                        subcategories = Subcategory.query.filter_by(category_id=category.id).all()
                        ps = Subcategory.query.filter_by(subcategory_name=parent_subcategory_name).first()
                        if subcategories and ps is None:
                            return jsonify([{'id': subcategory.id, 'subcategory_name': subcategory.subcategory_name, 'category_id': subcategory.category_id} for subcategory in subcategories])



                else:
                    categories = Category.query.filter_by(space_id=space.id).all()
                    return jsonify([{'id': category.id, 'category_name': category.category_name, 'space_id': category.space_id} for category in categories])

            else:
                return jsonify({'message': 'Space not found'}), 404




api.add_resource(SpaceResource, '/space', '/space/<string:space_name>')
api.add_resource(CategoryResource, '/space/<string:space_name>/category', '/category')
api.add_resource(SubcategoryResource, '/<string:category_name>/subcategory', '/subcategory', '/<string:category_name>/<string:parent_subcategory_name>/subcategory', '/<string:parent_subcategory_name>/subcategory','/space/<string:space_name>/category/<string:category_name>/subcategory','/space/<string:space_name>/category/<string:category_name>/<string:parent_subcategory_name>/subcategory')





if __name__ == '__main__':
    app.run(debug=True)