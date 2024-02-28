from main import *
class UrlResource(Resource):
    def get(self):
        urls = Url.query.all()
        return [url.__dict__ for url in urls]
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('link', type=str, required=True)
        parser.add_argument('image', type=str, required=False)
        parser.add_argument('category_id', type=int, required=True)
        parser.add_argument('category_name', type=str, required=True)
        parser.add_argument('subcategory_id', type=int, required=True)
        parser.add_argument('subcategory_name', type=str, required=True)
        args = parser.parse_args()
        url = Url(name=args['name'], link=args['link'], image=args['image'], category_id=args['category_id'], category_name=args['category_name'], subcategory_id=args['subcategory_id'], subcategory_name=args['subcategory_name'])
        db.session.add(url)
        db.session.commit()
        return url.__dict__