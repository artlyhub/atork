from rest_framework import serializers

from crowdfund.models import FundItem, Funder


class FundItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundItem
        fields = ('artist',
                  'image',
                  'name',
                  'material',
                  'year',
                  'size',
                  'estimate_min_price',
                  'estimate_max_price',
                  'hammer_price',)


class FunderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funder
        fields = ('funditem',
                  'funder_name',
                  'date',
                  'amount',)
