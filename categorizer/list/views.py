from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Space, Category, Subcategory, Url
from .serializers import SpaceSerializer, CategorySerializer, SubcategorySerializer, UrlSerializer
from urllib.parse import urlparse

class SpaceList(APIView):
    def get(self, request):
        spaces = Space.objects.all()
        serializer = SpaceSerializer(spaces, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SpaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SpaceDetail(APIView):
    def get_object(self, space_name):
        try:
            return Space.objects.get(space_name=space_name)
        except Space.DoesNotExist:
            return None

    def get(self, request, space_name):
        space = self.get_object(space_name)
        if space is not None:
            serializer = SpaceSerializer(space)
            return Response(serializer.data)
        return Response({'message': 'Space not found'}, status=status.HTTP_404_NOT_FOUND)

class CategoryList(APIView):
    def get(self, request, space_name=None):
        if space_name:
            space = Space.objects.filter(space_name=space_name).first()
            if space:
                categories = Category.objects.filter(space=space)
                serializer = CategorySerializer(categories, many=True)
                return Response(serializer.data)
            return Response({'message': 'Space not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data)

    def post(self, request, space_name):
        space = Space.objects.filter(space_name=space_name).first()
        if space:
            data = request.data
            data['space'] = space.id
            serializer = CategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Space not found'}, status=status.HTTP_404_NOT_FOUND)

class SubcategoryList(APIView):
    def get(self, request, space_name=None, category_name=None):
        if space_name:
            space = Space.objects.filter(space_name=space_name).first()
            if space:
                if category_name:
                    category = Category.objects.filter(category_name=category_name, space=space).first()
                    if category:
                        subcategories = Subcategory.objects.filter(category=category, parent_subcategory=None)
                        serializer = SubcategorySerializer(subcategories, many=True)
                        return Response(serializer.data)
                    else:
                        return Response({'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({'message': 'Category name required'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Space not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            subcategories = Subcategory.objects.all()
            serializer = SubcategorySerializer(subcategories, many=True)
            return Response(serializer.data)

    def post(self, request, space_name, category_name):
        space = Space.objects.filter(space_name=space_name).first()
        if space:
            category = Category.objects.filter(category_name=category_name, space=space).first()
            if category:
                data = request.data
                data['category'] = category.id
                serializer = SubcategorySerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Space not found'}, status=status.HTTP_404_NOT_FOUND)

class UrlList(APIView):
    def get(self, request, space_name=None, category_name=None, subcategory_name=None):
        if space_name:
            space = Space.objects.filter(space_name=space_name).first()
            if space:
                if category_name:
                    category = Category.objects.filter(category_name=category_name, space=space).first()
                    if category:
                        if subcategory_name:
                            subcategory = Subcategory.objects.filter(subcategory_name=subcategory_name, category=category).first()
                            if subcategory:
                                urls = Url.objects.filter(subcategory=subcategory)
                                serializer = UrlSerializer(urls, many=True)
                                return Response(serializer.data)
                            else:
                                return Response({'message': 'Subcategory not found'}, status=status.HTTP_404_NOT_FOUND)
                        else:
                            urls = Url.objects.filter(category=category)
                            serializer = UrlSerializer(urls, many=True)
                            return Response(serializer.data)
                    else:
                        return Response({'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
                else:
                    categories = Category.objects.filter(space=space)
                    serializer = CategorySerializer(categories, many=True)
                    return Response(serializer.data)
            else:
                return Response({'message': 'Space not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            urls = Url.objects.all()
            serializer = UrlSerializer(urls, many=True)
            return Response(serializer.data)

    def post(self, request, space_name, category_name, subcategory_name=None):
        link = request.data.get('link')
        name = urlparse(link).netloc.replace(".com", "")
        image = show_image(link)  # Assuming you have a function to get the image
        space = Space.objects.filter(space_name=space_name).first()
        if space:
            category = Category.objects.filter(category_name=category_name, space=space).first()
            if category:
                data = request.data
                data['name'] = name
                data['image'] = image
                data['category'] = category.id
                if subcategory_name:
                    subcategory = Subcategory.objects.filter(subcategory_name=subcategory_name, category=category).first()
                    if subcategory:
                        data['subcategory'] = subcategory.id
                    else:
                        return Response({'message': 'Subcategory not found'}, status=status.HTTP_404_NOT_FOUND)
                serializer = UrlSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Space not found'}, status=status.HTTP_404_NOT_FOUND)
