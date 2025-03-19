from product.models import ProductBrand 
from bson import ObjectId


class BrandRepository:
    
    @staticmethod
    def create_brand(validated_data):
        brand = ProductBrand(**validated_data)
        brand.save()
        return brand

    @staticmethod
    def get_id(brand_id):
        try:
            return ProductBrand.objects.get(id=ObjectId(brand_id))
        except ProductBrand.DoesNotExist:
            return None
    
    @staticmethod
    def update_brand(brand,validated_data):
        for key,value in validated_data.items():
            setattr(brand,key,value)   
        brand.save()
        return brand

    @staticmethod
    def get_all():
        return ProductBrand.objects.all()

    @staticmethod
    def delete_brand(brand):
        return brand.delete()

    @staticmethod
    def get_by_name(name):
        try:   
            return ProductBrand.objects.get(name=name)
        except ProductBrand.DoesNotExist:
            return None
    