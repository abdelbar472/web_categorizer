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
        def get(self, space_name=None, category_name=None, parent_subcategory_name=None):
            if space_name:
                space = Space.query.filter_by(space_name=space_name).first()
                if space:
                    if category_name:
                        category = Category.query.filter_by(category_name=category_name).first()
                        if category:
                            subcategories = Subcategory.query.filter_by(category_id=category.id,
                                                                        parent_subcategory_id=None).all()
                            return jsonify([{'id': subcategory.id, 'subcategory_name': subcategory.subcategory_name,
                                             'category_id': subcategory.category_id} for subcategory in subcategories])
                        else:
                            if parent_subcategory_name:
                                parent_subcategory = Subcategory.query.filter_by(subcategory_name=parent_subcategory_name).first()
                                if parent_subcategory:
                                    subcategories = Subcategory.query.filter_by(parent_subcategory_id=parent_subcategory.id).all()
                                    return jsonify([{'id': subcategory.id,
                                                     'subcategory_name': subcategory.subcategory_name,
                                                     'category_id': subcategory.category_id,
                                                     'parent_subcategory_name': parent_subcategory.subcategory_name} for
                                                    subcategory in subcategories])
                                else:
                                    return jsonify({'message': 'Parent subcategory not found'}), 404
                            else:
                                subcategories = Subcategory.query.filter_by(category_id=category.id).all()
                                return jsonify([{'id': subcategory.id, 'subcategory_name': subcategory.subcategory_name,
                                                 'category_id': subcategory.category_id} for subcategory in
                                                subcategories])
                    else:
                        categories = Category.query.filter_by(space_id=space.id).all()
                        return jsonify(
                            [{'id': category.id, 'category_name': category.category_name, 'space_id': category.space_id}
                             for category in categories])
                else:
                    return jsonify({'message': 'Space not found'}), 404

        def post(self, space_name, category_name, parent_subcategory_name=None):
            parser = reqparse.RequestParser()
            parser.add_argument('subcategory_name', type=str, required=True)
            args = parser.parse_args()
            space = Space.query.filter_by(space_name=space_name).first()
            if space:
                category = Category.query.filter_by(category_name=category_name).first()
                if category:
                    if parent_subcategory_name:
                        parent_subcategory = Subcategory.query.filter_by(subcategory_name=parent_subcategory_name).first()
                        if parent_subcategory:
                            subcategory = Subcategory(subcategory_name=args['subcategory_name'], category_id=category.id,
                                                      parent_subcategory_id=parent_subcategory.id)
                            db.session.add(subcategory)
                            db.session.commit()
                            return jsonify({'id': subcategory.id, 'subcategory_name': subcategory.subcategory_name,
                                            'category_id': subcategory.category_id,
                                            'parent_subcategory_name': parent_subcategory.subcategory_name})
                        else:
                            return jsonify({'message': 'Parent subcategory not found'}), 404
                    else:
                        subcategory = Subcategory(subcategory_name=args['subcategory_name'], category_id=category.id)
                        db.session.add(subcategory)
                        db.session.commit()
                        return jsonify({'id': subcategory.id, 'subcategory_name': subcategory.subcategory_name,
                                        'category_id': subcategory.category_id})
                else:
                    return jsonify({'message': 'Category not found'}), 404
            else:
                return jsonify({'message': 'Space not found'}), 404


api.add_resource(SpaceResource, '/space', '/space/<string:space_name>')
api.add_resource(CategoryResource, '/space/<string:space_name>/category', '/category')
api.add_resource(SubcategoryResource,'/space/<string:space_name>/category/<string:category_name>/subcategory','/space/<string:space_name>/category/<string:category_name>/subcategory/<string:parent_subcategory_name>')





if __name__ == '__main__':
    app.run(debug=True)

    '''class SubcategoryResource(Resource):
    def get(self, space_name=None, category_name=None, parent_subcategory_name=None):
        if space_name:
            space = Space.query.filter_by(space_name=space_name).first()
            if space:
                if category_name:
                    category = Category.query.filter_by(category_name=category_name).first()
                    if category:
                        if parent_subcategory_name:
                            parent_subcategory = Subcategory.query.filter_by(subcategory_name=parent_subcategory_name).first()
                            if parent_subcategory:
                                subcategories = Subcategory.query.filter_by(parent_subcategory_id=parent_subcategory.id).all()
                                return jsonify([{'id': subcategory.id, 'subcategory_name': subcategory.subcategory_name, 'category_id': subcategory.category_id, 'parent_subcategory_name': parent_subcategory.subcategory_name} for subcategory in subcategories])
                            else:
                                return jsonify({'message': 'Parent subcategory not found'}), 404
                        else:
                            subcategories = Subcategory.query.filter_by(category_id=category.id).all()
                            return jsonify([{'id': subcategory.id, 'subcategory_name': subcategory.subcategory_name, 'category_id': subcategory.category_id} for subcategory in subcategories])
                else:
                    categories = Category.query.filter_by(space_id=space.id).all()
                    return jsonify([{'id': category.id, 'category_name': category.category_name, 'space_id': category.space_id} for category in categories])
            else:
                return jsonify({'message': 'Space not found'}), 404'''