from rest_framework import serializers
from bson import ObjectId

class CategorySerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    title=serializers.CharField(max_length=255)
    description = serializers.CharField()
    image_url = serializers.CharField(required=False)
    
    def get_id(self, obj):
        return str(obj.id)
    
    def validate(self,data):
        if 'title' in data and not data['title'].strip():
            raise serializers.ValidationError("Category title cannot be empty.")
        
        if 'title' in data and any(char.isdigit() for char in data['title']):
            raise serializers.ValidationError("Category title cannot contain numbers.")
        return data
    
class BrandSerializer(serializers.Serializer):
    category=serializers.CharField()
    name=serializers.CharField()
    image_url = serializers.CharField(required=False)
    
    def validate_name(self,value):
        if not value.strip():
            raise serializers.ValidationError("Brand name cannot be empty.")
        return value
    
    def validate_category(self,value):
        from product.models import ProductCategory
        if ObjectId.is_valid(value):
            category=ProductCategory.objects(id=value).first()
        
        if not category:
            raise serializers.ValidationError("Invalid category. Category does not have existence.")

        return category    
        
class ProductSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.IntegerField()
    category = serializers.CharField()
    brand = serializers.CharField(max_length=100)
    quantity = serializers.IntegerField()
    initial_quantity = serializers.IntegerField(read_only=True)
    image_url = serializers.CharField(required=False)
    
    def get_id(self, obj):
        return str(obj.id)
    
    def validate(self, data):
        special_characters = "!@#$%^&*()_+=-"
        if 'name' in data and any(c in special_characters for c in data['name']):
            raise serializers.ValidationError({"name": "Name cannot contain special characters"})

        if 'price' in data and data['price'] < 0:
            raise serializers.ValidationError({"price": "Price should be greater than 0"})

        if 'quantity' in data and data['quantity'] < 0:
            raise serializers.ValidationError({"quantity": "Quantity should be greater than 0"})
        return data

    def validate_category(self, value):
        from product.models import ProductCategory
        if ObjectId.is_valid(value):
            category = ProductCategory.objects(id=value).first()
            
        if not category:
            raise serializers.ValidationError("Invalid category. Category does not exist.")

        return category
    
    def validate_brand(self, value):
        from product.models import ProductBrand
        if ObjectId.is_valid(value):
            brand = ProductBrand.objects(id=value).first()
            
        if not brand:
            raise serializers.ValidationError("Invalid brand. Brand does not exist.")

        return brand


class UserSignupSerializer(serializers.Serializer):
     id=serializers.SerializerMethodField()
     username = serializers.CharField()
     password = serializers.CharField(write_only=True)
     
     def validate(self,data):
        if 'username' in data and not data['username'].strip():
            raise serializers.ValidationError("Username cannot be empty.")
        return data

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
       
   
