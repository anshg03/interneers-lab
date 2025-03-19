from product.models import ProductCategory 
from bson import ObjectId

class CategoryRepository:
    
    @staticmethod
    def create_category(validated_data):
        category = ProductCategory(**validated_data)
        category.save()
        return category
    
    @staticmethod
    def get_id(category_id):
        try:
            return ProductCategory.objects.get(id=ObjectId(category_id))
        except ProductCategory.DoesNotExist:
            return None
        
    @staticmethod
    def update_category(category,validated_data):
        for key,value in validated_data.items():
            setattr(category,key,value)   
        category.save()
        return category
    
    @staticmethod
    def get_all():
        return ProductCategory.objects.all()
    
    @staticmethod
    def delete_category(category):
        return category.delete()

    @staticmethod
    def get_by_name(title):
        try:   
            return ProductCategory.objects.get(title=title)
        except ProductCategory.DoesNotExist:
            return None

    