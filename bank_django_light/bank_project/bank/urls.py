from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bank import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'bankaccounts', views.BankAccountViewSet)
#router.register(r'accounts', views.BankAccountViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('bankaccounts/<int:pk>/deposit/', views.BankAccountViewSet.as_view({'post': 'deposit'}), name='bankaccount-deposit'),
    path('bankaccounts/<int:pk>/withdraw/', views.BankAccountViewSet.as_view({'post': 'withdraw'}), name='bankaccount-withdraw'),
    path('bankaccounts/<int:pk>/transfer/', views.BankAccountViewSet.as_view({'post': 'transfer'}), name='bankaccount-transfer'),
    path('bankaccounts/create/', views.BankAccountViewSet.as_view({'post': 'create_account'}), name='bankaccount-create_account'),
]
