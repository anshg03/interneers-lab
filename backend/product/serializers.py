from rest_framework import serializers
from .models import Product 

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__' 
        
    def validate(self,data):
        
        special_characters="!@#$%^&*()_+=-"
        if any(c in special_characters for c in data['name']):
            raise serializers.ValidationError('name cannot contain special char')
        
        
        if 'price' in data and data['price'] < 0:
            raise serializers.ValidationError('price should be more than 0')
        
        return data