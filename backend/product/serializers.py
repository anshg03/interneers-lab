from rest_framework import serializers

class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.IntegerField()
    category = serializers.CharField(max_length=100)
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

    # def create(self, validated_data):
    #     #calls while invoking create 
    #     from product.models import Product  
    #     product = Product(**validated_data)
    #     product.save()
    #     return product
    
    # def update(self,instance,validated_data):
    #     #calls while updating
    #     for key, value in validated_data.items():
    #         setattr(instance, key, value)
    #     instance.save()
    #     return instance
        
   
