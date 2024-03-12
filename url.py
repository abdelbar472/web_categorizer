from main import *
class UrlResource(Resource):
    def get(self, space_name=None, category_name=None, subcategory_name=None):
        if space_name:
            space = Space.query.filter_by(space_name=space_name).first()
            if space:
                if category_name:
                    category = Category.query.filter_by(category_name=category_name).first()
                    if category:
                        if subcategory_name:
                            subcategory = Subcategory.query.filter_by(subcategory_name=subcategory_name).first()
                            if subcategory:
                                urls = Url.query.filter_by(subcategory_id=subcategory.id).all()
                                return jsonify([{'id': url.id, 'name': url.name, 'link': url.link, 'image': url.image, 'category_id': url.category_id, 'category_name': url.category_name, 'subcategory_id': url.subcategory_id, 'subcategory_name': url.subcategory_name} for url in urls])
                            else:
                                return jsonify({'message': 'Subcategory not found'}), 404
                        else:
                            urls = Url.query.filter_by(category_id=category.id).all()
                            return jsonify([{'id': url.id, 'name': url.name, 'link': url.link, 'image': url.image, 'category_id': url.category_id, 'category_name': url.category_name, 'subcategory_id': url.subcategory_id, 'subcategory_name': url.subcategory_name} for url in urls])
                else:
                    categories = Category.query.filter_by(space_id=space.id).all()
                    return jsonify([{'id': category.id, 'category_name': category.category_name, 'space_id': category.space_id} for category in categories])
            else:
                return jsonify({'message': 'Space not found'}), 404
        else:
            urls = Url.query.all()
            return jsonify([{'id': url.id, 'name': url.name, 'link': url.link, 'image': url.image, 'category_id': url.category_id, 'category_name': url.category_name, 'subcategory_id': url.subcategory_id, 'subcategory_name': url.subcategory_name} for url in urls])

    def post(self, space_name, category_name, subcategory_name=None):
        parser = reqparse.RequestParser()
        parser.add_argument('link', type=str, required=True)
        args = parser.parse_args()

        def get_website_name(url):
            """
            Get the website name from the given URL.

            Args:
                url (str): The URL of the website.

            Returns:
                str: The website name.
            """
            parsed_url = urlparse(url)
            if parsed_url.netloc:
                return parsed_url.netloc.replace(".com", "")
            return "Invalid URL"

        name = get_website_name(args['link'])

        def show_image(image_url):
            """
            Display the image from the given URL.

            Args:
                image_url (str): The URL of the image.
            """
            try:
                # Make an HTTP request to the URL with a timeout of 5 seconds
                response = requests.get(image_url, timeout=5)

                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    # Read the image content from the response
                    image_content = response.content

                    # Create a PIL Image object from the image content
                    image = Image.open(BytesIO(image_content))

                    # Display the image
                    # image.show()
                else:
                    print(f"Failed to download image. Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")

        space = Space.query.filter_by(space_name=space_name).first()
        if space:
            category = Category.query.filter_by(category_name=category_name, space_id=space.id).first()
            if category:
                new_url = Url(name=name, link=args['link'], category_id=category.id,
                              category_name=category.category_name)
                db.session.add(new_url)
                db.session.commit()

                return jsonify({'message': 'URL added',
                                'url': {'id': new_url.id, 'name': new_url.name, 'link': new_url.link,
                                        'category_id': new_url.category_id,
                                        'category_name': new_url.category_name}}), 201
            else:
                return jsonify({'message': 'Category not found'}), 404
        else:
            return jsonify({'message': 'Space not found'}), 404



'''
def show_image(image_url):
    """
    Display the image from the given URL.
    
    Args:
        image_url (str): The URL of the image.
    """
    try:
        # Make an HTTP request to the URL with a timeout of 5 seconds
        response = requests.get(image_url, timeout=5)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Read the image content from the response
            image_content = response.content

            # Create a PIL Image object from the image content
            image = Image.open(BytesIO(image_content))

            # Display the image
            # image.show()
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        '''