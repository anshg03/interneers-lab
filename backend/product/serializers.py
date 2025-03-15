from rest_framework import serializers


class CategorySerializer(serializers.Serializer):
    title=serializers.CharField(max_length=255)
    description = serializers.CharField()
    
    def validate(self,data):
        if 'title' in data and not data['title'].strip():
            raise serializers.ValidationError("Category title cannot be empty.")
        
        if 'title' in data and any(char.isdigit() for char in data['title']):
            raise serializers.ValidationError("Category title cannot contain numbers.")
        return data
    

class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.IntegerField()
    category = CategorySerializer()
    brand = serializers.CharField(max_length=100)
    quantity = serializers.IntegerField()
    initial_quantity = serializers.IntegerField(read_only=True)
    
    
    def validate(self, data):
        special_characters = "!@#$%^&*()_+=-"
        if 'name' in data and any(c in special_characters for c in data['name']):
            raise serializers.ValidationError({"name": "Name cannot contain special characters"})

        if 'price' in data and data['price'] < 0:
            raise serializers.ValidationError({"price": "Price should be greater than 0"})

        if 'quantity' in data and data['quantity'] < 0:
            raise serializers.ValidationError({"quantity": "Quantity should be greater than 0"})
        return data

        
   
