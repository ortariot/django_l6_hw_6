from rest_framework import serializers
from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']



class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    # настройте сериализатор для склада

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)
        for item in positions:
            new_stok_product = StockProduct.\
                objects.create(product=item['product'],
                               stock=stock,
                               quantity=item['quantity'],
                               price=item['price']
                               )
            stock.positions.add(new_stok_product)

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        print(type(stock))
        for item in positions:
            StockProduct.\
              objects.update_or_create(defaults={'quantity': item['quantity'],
                                                 'price': item['price']
                                                 },
                                       product=item['product'],
                                       stock=stock
                                       )
        return stock

    class Meta:
        model = Stock
        fields = ["address", "positions"]
