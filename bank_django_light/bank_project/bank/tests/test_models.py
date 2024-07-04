from django.test import TestCase
from bank.models import User, BankAccount

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='testuser', password='12345')
        self.assertEqual(user.username, 'testuser')

class BankAccountModelTest(TestCase):
    def test_create_account(self):
        user = User.objects.create_user(username='testuser', password='12345')
        account = BankAccount.objects.create(user=user, account_number='1234567890')
        self.assertEqual(account.user, user)
        self.assertEqual(account.balance, 0.00)
