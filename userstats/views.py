from rest_framework.views import APIView
from datetime import datetime
from expenses.models import Expense
from rest_framework.response import Response
from rest_framework import status


class ExpenseSummaryStats(APIView):

    def get_amount_for_category(self, expense_list, category):
        expenses = expense_list.filter(category=category)
        amount = 0
        
        

    def get_category(self, expense):
        return expense.category

    def get(self, request):
        todays_date = datetime.date.today()
        years_ago = todays_date - datetime.timedelta(day=30*12)
        expenses = Expense.objects.filter(
            owner=request.user, date__gte=years_ago, date__lte=todays_date)

        final = {}

        categories = list(set(map(self.get_category, expenses)))

        for expense in expenses:
            for category in categories:
                final[category] = self.get_amount_for_category(
                    expenses, category)

        return Response({'category_data': final}, status=status.HTTP_200_OK)
