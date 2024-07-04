# # from django.urls import reverse
# # from rest_framework.test import APITestCase
# # from rest_framework import status
# # from bank.models import User, BankAccount

# # class UserViewSetTest(APITestCase):
# #     def test_register_user(self):
# #         url = reverse('user-list')
# #         data = {'username': 'testuser', 'password': '12345'}
# #         response = self.client.post(url, data, format='json')
# #         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# #     def test_login_user(self):
# #         user = User.objects.create_user(username='testuser', password='12345')
# #         url = reverse('user-login')
# #         data = {'username': 'testuser', 'password': '12345'}
# #         response = self.client.post(url, data, format='json')
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)

# # class BankAccountViewSetTest(APITestCase):
# #     def setUp(self):
# #         self.user = User.objects.create_user(username='testuser', password='12345')
# #         self.account = BankAccount.objects.create(user=self.user, account_number='1234567890')

# #     def test_create_account(self):
# #         url = reverse('bankaccount-list')
# #         self.client.force_authenticate(user=self.user)
# #         data = {'account_number': '0987654321'}
# #         response = self.client.post(url, data, format='json')
# #         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# #     def test_deposit(self):
# #         url = reverse('bankaccount-deposit', args=[self.account.id])
# #         self.client.force_authenticate(user=self.user)
# #         data = {'amount': 100.00}
# #         response = self.client.post(url, data, format='json')
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)
# #         self.account.refresh_from_db()
# #         self.assertEqual(self.account.balance, 100.00)

# #     def test_withdraw(self):
# #         self.account.balance = 200.00
# #         self.account.save()
# #         url = reverse('bankaccount-withdraw', args=[self.account.id])
# #         self.client.force_authenticate(user=self.user)
# #         data = {'amount': 50.00}
# #         response = self.client.post(url, data, format='json')
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)
# #         self.account.refresh_from_db()
# #         self.assertEqual(self.account.balance, 150.00)

# #     def test_transfer(self):
# #         target_account = BankAccount.objects.create(user=self.user, account_number='0987654321')
# #         self.account.balance = 200.00
# #         self.account.save()
# #         url = reverse('bankaccount-transfer', args=[self.account.id])
# #         self.client.force_authenticate(user=self.user)
# #         data = {'target_account_number': target_account.account_number, 'amount': 50.00}
# #         response = self.client.post(url, data, format='json')
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)
# #         self.account.refresh_from_db()
# #         target_account.refresh_from_db()
# #         self.assertEqual(self.account.balance, 150.00)
# #         self.assertEqual(target_account.balance, 50.00)

# from django.urls import reverse
# from rest_framework.test import APITestCase
# from rest_framework import status
# from bank.models import User, BankAccount
# from rest_framework_simplejwt.tokens import RefreshToken
# import json

# class UserViewSetTest(APITestCase):
#     def setUp(self):
#         self.register_url = reverse('user-list')
#         self.login_url = reverse('user-login')
#         self.user = User.objects.create_user(username='testuser', password='12345')
#         self.client.login(username='testuser', password='12345')

#     def test_register_user(self):
#         data = {'username': 'newuser', 'password': '12345'}
#         response = self.client.post(self.register_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_register_user_with_existing_username(self):
#         data = {'username': 'testuser', 'password': '12345'}
#         response = self.client.post(self.register_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_login_user(self):
#         data = {'username': 'testuser', 'password': '12345'}
#         response = self.client.post(self.login_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_login_with_invalid_credentials(self):
#         data = {'username': 'testuser', 'password': 'wrongpassword'}
#         response = self.client.post(self.login_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# class BankAccountViewSetTest(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='12345')
#         self.token = RefreshToken.for_user(self.user).access_token
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
#         self.account = BankAccount.objects.create(user=self.user, account_number='1234567890')
#         self.create_account_url = reverse('bankaccount-create_account')
#         self.deposit_url = reverse('bankaccount-deposit', args=[self.account.id])
#         self.withdraw_url = reverse('bankaccount-withdraw', args=[self.account.id])
#         self.transfer_url = reverse('bankaccount-transfer', args=[self.account.id])

#     def test_create_account(self):
#         data = {'user_id': self.user.id}
#         response = self.client.post(self.create_account_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_create_account_with_invalid_user(self):
#         data = {'user_id': 9999}
#         response = self.client.post(self.create_account_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_deposit(self):
#         data = {'amount': '100.00'}
#         response = self.client.post(self.deposit_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.account.refresh_from_db()
#         self.assertEqual(self.account.balance, 100.00)

#     def test_deposit_with_invalid_amount(self):
#         data = {'amount': 'invalid'}
#         response = self.client.post(self.deposit_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_withdraw(self):
#         self.account.balance = 200.00
#         self.account.save()
#         data = {'amount': '50.00'}
#         response = self.client.post(self.withdraw_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.account.refresh_from_db()
#         self.assertEqual(self.account.balance, 150.00)

#     def test_withdraw_insufficient_funds(self):
#         data = {'amount': '300.00'}
#         response = self.client.post(self.withdraw_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_transfer(self):
#         target_account = BankAccount.objects.create(user=self.user, account_number='0987654321')
#         self.account.balance = 200.00
#         self.account.save()
#         data = {'target_account_number': target_account.account_number, 'amount': '50.00'}
#         response = self.client.post(self.transfer_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.account.refresh_from_db()
#         target_account.refresh_from_db()
#         self.assertEqual(self.account.balance, 150.00)
#         self.assertEqual(target_account.balance, 50.00)

#     def test_transfer_insufficient_funds(self):
#         target_account = BankAccount.objects.create(user=self.user, account_number='0987654321')
#         data = {'target_account_number': target_account.account_number, 'amount': '300.00'}
#         response = self.client.post(self.transfer_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_transfer_to_nonexistent_account(self):
#         data = {'target_account_number': 'nonexistent', 'amount': '50.00'}
#         response = self.client.post(self.transfer_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from bank.models import User, BankAccount

class UserViewSetTest(APITestCase):
    def test_register_user(self):
        url = reverse('user-list')
        data = {'username': 'testuser', 'password': '12345'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        user = User.objects.create_user(username='testuser', password='12345')
        url = reverse('user-login')
        data = {'username': 'testuser', 'password': '12345'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class BankAccountViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.account = BankAccount.objects.create(user=self.user, account_number='1234567890')
        self.create_account_url = reverse('bankaccount-create_account')
        self.deposit_url = reverse('bankaccount-deposit', args=[self.account.id])
        self.withdraw_url = reverse('bankaccount-withdraw', args=[self.account.id])
        self.transfer_url = reverse('bankaccount-transfer', args=[self.account.id])

    def test_create_account(self):
        self.client.force_authenticate(user=self.user)
        data = {'user_id': self.user.id}
        response = self.client.post(self.create_account_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_account_with_invalid_user(self):
        self.client.force_authenticate(user=self.user)
        data = {'user_id': 999}  # Assuming 999 is an invalid user ID
        response = self.client.post(self.create_account_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_deposit(self):
        self.client.force_authenticate(user=self.user)
        data = {'amount': 100.00}
        response = self.client.post(self.deposit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 100.00)

    def test_deposit_with_invalid_amount(self):
        self.client.force_authenticate(user=self.user)
        data = {'amount': 'invalid'}  # Invalid amount
        response = self.client.post(self.deposit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_withdraw(self):
        self.account.balance = 200.00
        self.account.save()
        self.client.force_authenticate(user=self.user)
        data = {'amount': 50.00}
        response = self.client.post(self.withdraw_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 150.00)

    def test_withdraw_insufficient_funds(self):
        self.client.force_authenticate(user=self.user)
        data = {'amount': 50.00}
        response = self.client.post(self.withdraw_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_transfer(self):
        target_account = BankAccount.objects.create(user=self.user, account_number='0987654321')
        self.account.balance = 200.00
        self.account.save()
        self.client.force_authenticate(user=self.user)
        data = {'target_account_number': target_account.account_number, 'amount': 50.00}
        response = self.client.post(self.transfer_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.account.refresh_from_db()
        target_account.refresh_from_db()
        self.assertEqual(self.account.balance, 150.00)
        self.assertEqual(target_account.balance, 50.00)

    def test_transfer_insufficient_funds(self):
        target_account = BankAccount.objects.create(user=self.user, account_number='0987654321')
        self.client.force_authenticate(user=self.user)
        data = {'target_account_number': target_account.account_number, 'amount': 50.00}
        response = self.client.post(self.transfer_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_transfer_to_nonexistent_account(self):
        self.account.balance = 200.00
        self.account.save()
        self.client.force_authenticate(user=self.user)
        data = {'target_account_number': 'nonexistent', 'amount': 50.00}
        response = self.client.post(self.transfer_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
