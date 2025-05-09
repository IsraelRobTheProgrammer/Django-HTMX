from django.shortcuts import render
from .models import Transaction
from django.contrib.auth.decorators import login_required
from .filters import TransactionFilter


# Create your views here.
def index(request):
    return render(request, "tracker/index.html")


@login_required
def transactions_list(request):
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(
            user=request.user,
        ).select_related("category"),
    )
    transaction_filter
    total_income = transaction_filter.qs.get_total_income()
    total_expenses = transaction_filter.qs.get_total_expenses()

    context = {
        "filter": transaction_filter,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_income": total_income - total_expenses,
    }
    if request.htmx:
        return render(request, "tracker/partials/transactions_container.html", context)

    return render(request, "tracker/transactions_list.html", context)
