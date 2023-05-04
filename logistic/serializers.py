from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class StockProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = StockProductSerializer(many=True)

    class Meta:
        model = Stock
        fields = '__all__'

    def create(self, validated_data):
        positions_data = validated_data.pop('positions')
        stock = Stock.objects.create(**validated_data)
        for position_data in positions_data:
            product_data = position_data.pop('product')
            product = Product.objects.get_or_create(**product_data)[0]
            StockProduct.objects.create(stock=stock, product=product, **position_data)
        return stock

    def update(self, instance, validated_data):
        positions_data = validated_data.pop('positions')
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        current_positions = {p.product_id: p for p in instance.positions.all()}
        for position_data in positions_data:
            product_data = position_data.pop('product')
            product = Product.objects.get_or_create(**product_data)[0]
            quantity = position_data.get('quantity', 1)
            price = position_data.get('price', 0)
            if product.id in current_positions:
                # update existing position
                position = current_positions[product.id]
                position.quantity = quantity
                position.price = price
                position.save()
            else:
                # create new position
                StockProduct.objects.create(stock=instance, product=product, quantity=quantity, price=price)
        return instance
