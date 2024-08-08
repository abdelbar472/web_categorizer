from main import *


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