from rest_framework import routers
from django.urls import path, include

from tradeApi.views import UserWalletViewSet,BuyShareViewSet,SellShareViewSet,AddBalanceView,WithdrawBalanceView

router = routers.DefaultRouter()
router.register(r'user-wallets', UserWalletViewSet)
router.register(r'buy-shares', BuyShareViewSet)
router.register(r'sell-shares', SellShareViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('add-balance/<int:user_wallet_id>/', AddBalanceView.as_view(), name='add-balance'),
    path('withdraw-balance/<int:user_wallet_id>/', WithdrawBalanceView.as_view(), name='withdraw-balance'),
]