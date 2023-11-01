from rest_framework import viewsets

from .models import UserWallet,BuyShare,SellShare
from .serializers import UserWalletSerializer,BuyShareSerializer,SellShareSerializer,AddBalanceSerializer,WithdrawBalanceSerializer
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from .models import UserWallet
from rest_framework import status

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class AddBalanceView(APIView):
    def post(self, request, user_wallet_id):
        try:
            user_wallet = UserWallet.objects.get(pk=user_wallet_id)
        except UserWallet.DoesNotExist:
            return Response({"error": "UserWallet not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AddBalanceSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            user_wallet.balance += amount
            user_wallet.save()
            return Response({"message": "Balance added successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WithdrawBalanceView(APIView):
    def post(self, request, user_wallet_id):
        try:
            user_wallet = UserWallet.objects.get(pk=user_wallet_id)
        except UserWallet.DoesNotExist:
            return Response({"error": "UserWallet not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = WithdrawBalanceSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            if user_wallet.balance >= amount:
                user_wallet.balance -= amount
                user_wallet.save()
                return Response({"message": "Balance withdraw successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "This amount is not availabe in your wallet"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserWalletViewSet(viewsets.ModelViewSet):
    queryset = UserWallet.objects.all()
    serializer_class = UserWalletSerializer
    
    

class BuyShareViewSet(viewsets.ModelViewSet):
    queryset = BuyShare.objects.all()
    serializer_class = BuyShareSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_wallet = serializer.validated_data["user_wallet"]
        stock_name = serializer.validated_data["stock_name"]
        quantity = serializer.validated_data["quantity"]
        price = serializer.validated_data["price"]
        # print(user_wallet.balance)
        
        if user_wallet.balance < price * quantity:
            raise ValidationError("Insufficient balance.")
        
        try:
            # Try to get an existing BuyShare object based on user_wallet and stock_name
            buyshare = BuyShare.objects.get(user_wallet=user_wallet, stock_name=stock_name)

            # Update the existing BuyShare object
            avg_price = (buyshare.quantity * buyshare.price + quantity * price) / (buyshare.quantity + quantity)
            buyshare.quantity += quantity
            buyshare.price = avg_price
            buyshare.save()

        except BuyShare.DoesNotExist:
            # If there is no existing BuyShare, create a new one
            buyshare = serializer.save()
            # print(buyshare)

        # Decrement the user's wallet balance by the price of the shares they are buying.
        user_wallet.balance -= serializer.validated_data["price"] * serializer.validated_data["quantity"]
        user_wallet.save()

        return Response(buyshare.id, status=status.HTTP_201_CREATED)
    

class SellShareViewSet(viewsets.ModelViewSet):
    queryset = SellShare.objects.all()
    serializer_class = SellShareSerializer
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_wallet = serializer.validated_data['user_wallet']
        stock_name = serializer.validated_data["stock_name"]
        quantity = serializer.validated_data["quantity"]
        price = serializer.validated_data["price"]

        # Check if the user wallet exists.
        try:
            user_wallet = UserWallet.objects.get(user=user_wallet)
        except UserWallet.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has enough shares of the stock to sell.
        try:
            buyshare = BuyShare.objects.get(user_wallet=user_wallet, stock_name=stock_name)
        except BuyShare.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if buyshare.quantity < quantity:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif buyshare.quantity == quantity:
            buyshare.delete()
        else:
            buyshare.quantity -= quantity
            buyshare.save()
        # Update the BuyShare model to reflect the sale.
        

        # Update the user's wallet balance to reflect the proceeds from the sale.
        user_wallet.balance += quantity * price
        user_wallet.save()

        # Create the SellShare object.
        sell_share = SellShare(
            user_wallet=user_wallet,
            stock_name=stock_name,
            quantity=quantity,
            price=price
        )
        sell_share.save()

        # Return the SellShare object.
        serializer = SellShareSerializer(sell_share)
        return Response(serializer.data, status=status.HTTP_201_CREATED)