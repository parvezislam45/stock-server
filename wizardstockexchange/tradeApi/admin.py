from django.contrib import admin
from .models import UserWallet,BuyShare,SellShare

admin.site.register(UserWallet)
admin.site.register(BuyShare)
admin.site.register(SellShare)

