from rest_framework import serializers
from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта
    class Meta:
        model = Product
        fields = ['title', 'description']


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
        # print(instance)
        positions = validated_data.pop('positions')
        # print(validated_data)
        # print(positions)
        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        print(type(stock))
        for item in positions:
            sp = StockProduct.\
                objects.update_or_create(product=item['product'],
                                         stock=stock,
                                         quantity=item['quantity'],
                                         price=item['price']
                                         )
                                            

        # sp.objects.update(quantity=77)
        # print(sp)
# =======
#         # sp = stock.positions.get(product=2)
#         # sp.objects.update(quantity=77)
#         # print(positions[0])
#         for item in positions:
#             sp, flag = StockProduct.objects.\
#                 update_or_create(product=item['product'],
#                                  stock=stock,
#                                  quantity=item['quantity'],
#                                  price=item['price']
#                                  )

#             print(sp)                   
#             stock.positions.set([sp])
# >>>>>>> 0294ade3a2db5b6b55e0ac4c683377adc4b65f0d
        # for item in stock.positions.all():
        #     # item.quantity = positions[0]['quantity']
        #     # item.save()
        #     item = super().update(positions[0]) 

    
            

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock

    class Meta:
        model = Stock
        fields = ["address","positions"]

