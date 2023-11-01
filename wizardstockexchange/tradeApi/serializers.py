from rest_framework import serializers
from .models import BuyShare,UserWallet,SellShare

from rest_framework import serializers

class AddBalanceSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        min_value=0.01,  # Minimum allowed amount (you can adjust as needed)
        error_messages={
            'min_value': 'Amount must be greater than or equal to 0.01',
        }
    )

class WithdrawBalanceSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        min_value=0.01,  # Minimum allowed amount (you can adjust as needed)
        error_messages={
            'min_value': 'Amount must be greater than or equal to 0.01',
        }
    )

class UserWalletSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()
    class Meta:
        model = UserWallet
        fields = ['user','user_email', 'balance']
        
    def get_user_email(self, obj):
        return obj.user.email
    
class BuyShareSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()
    class Meta:
        model = BuyShare
        fields = ['id','user_wallet','stock_name', 'stock_symbol', 'quantity', 'price', 'created_at', 'updated_at', 'user_email']
    
    def get_user_email(self, obj):
        return obj.user_wallet.user.email

class SellShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellShare
        fields = ['id', 'user_wallet', 'stock_name', 'stock_symbol', 'quantity', 'price', 'created_at', 'updated_at']