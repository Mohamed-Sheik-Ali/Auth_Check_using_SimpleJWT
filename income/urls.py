from django.urls import path
from expenses.views import *
from income.views import IncomeDetailAPIView, IncomeListAPIView

urlpatterns = [
    path('', IncomeListAPIView.as_view(), name="incomes"),
    path('<int:id>/', IncomeDetailAPIView.as_view(), name="income")
]
