from django.db import models
from django.conf import settings
from accounts.models import CustomUser

class UserWallet(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='user_wallet_tradeapi'
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.user}"
    
class BuyShare(models.Model):
    user_wallet = models.ForeignKey(
        UserWallet,
        on_delete=models.CASCADE,
    )
    stock_name = models.CharField(max_length=255)
    stock_symbol = models.CharField(max_length=10)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=100, decimal_places=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    
    def __str__(self):
        return f"user_wallet: {self.user_wallet.user} Stock_name: {self.stock_name} Quantity: {self.quantity} Price: {self.price}"
   
class SellShare(models.Model):
    user_wallet = models.ForeignKey(
        UserWallet,
        on_delete=models.CASCADE,
    )
    stock_name = models.CharField(max_length=255)
    stock_symbol = models.CharField(max_length=10)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=100, decimal_places=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"user_wallet: {self.user_wallet.user} Stock_name: {self.stock_name} Quantity: {self.quantity} Price: {self.price}"