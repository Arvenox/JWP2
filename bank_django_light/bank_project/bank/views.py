from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from .models import User, BankAccount
from .serializers import UserSerializer, BankAccountSerializer
from django.contrib.auth import authenticate
import random
import uuid
from decimal import Decimal

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response(UserSerializer(user).data)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)


class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return BankAccount.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def create_account(self, request):
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            account_number = str(uuid.uuid4())
            balance = Decimal(random.uniform(100.0, 1000.0))
            account = BankAccount.objects.create(user=user, account_number=account_number, balance=balance)
            return Response(BankAccountSerializer(account).data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def deposit(self, request, pk=None):
        account = self.get_object()
        amount = request.data.get('amount')
        amount = Decimal(amount)
        account.balance += amount
        account.save()
        return Response(BankAccountSerializer(account).data)

    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def withdraw(self, request, pk=None):
        account = self.get_object()
        amount = request.data.get('amount')
        if account.balance >= Decimal(amount):
            account.balance -= Decimal(amount)
            account.save()
            return Response(BankAccountSerializer(account).data)
        return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def transfer(self, request, pk=None):
        source_account = self.get_object()
        target_account_number = request.data.get('target_account_number')
        amount = request.data.get('amount')
        try:
            target_account = BankAccount.objects.get(account_number=target_account_number)
            if source_account.balance >= Decimal(amount):
                source_account.balance -= Decimal(amount)
                target_account.balance += Decimal(amount)
                source_account.save()
                target_account.save()
                return Response(BankAccountSerializer(source_account).data)
            return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
        except BankAccount.DoesNotExist:
            return Response({'error': 'Target account not found'}, status=status.HTTP_404_NOT_FOUND)