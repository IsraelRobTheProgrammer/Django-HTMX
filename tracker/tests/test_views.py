"""
Test the views of the tracker app
"""

from django.urls import reverse
import pytest
from datetime import datetime, timedelta

from tracker.models import Category


@pytest.mark.django_db
def test_total_values_appear_on_list_page(user_transactions, client):
    user = user_transactions[0].user
    client.force_login(user)

    income_total = sum(t.amount for t in user_transactions if t.type == "income")
    expense_total = sum(t.amount for t in user_transactions if t.type == "expense")
    net = income_total - expense_total

    # test_url = reverse("tracker:transactions_list")
    url = reverse("transactions_list")
    print(
        {"url": url},
    )

    response = client.get(url)
    # print(response.context, "rsp_cn")

    assert response.context["total_income"] == income_total
    assert response.context["total_expenses"] == expense_total
    assert response.context["net_income"] == net


@pytest.mark.django_db
def test_transaction_type_filter(authenticate_user, client):
    # income check
    GET_params = {"transaction_type": "income"}
    url = reverse("transactions_list")
    response = client.get(url, GET_params)

    qs = response.context["filter"].qs

    for transaction in qs:
        assert transaction.type == "income"

    # expense check
    GET_params = {"transaction_type": "expense"}
    url = reverse("transactions_list")
    response = client.get(url, GET_params)

    qs = response.context["filter"].qs

    for transaction in qs:
        assert transaction.type == "expense"


@pytest.mark.django_db
def test_transaction_start_end_date_filter(authenticate_user, client):
    start_date_cutoff = datetime.now().date() - timedelta(days=120)
    GET_params = {"start_date": start_date_cutoff}
    url = reverse("transactions_list")

    response = client.get(url, GET_params)

    qs = response.context["filter"].qs

    for transaction in qs:
        assert transaction.date >= start_date_cutoff

    end_date_cutoff = datetime.now().date() - timedelta(days=20)
    GET_params = {"end_date": end_date_cutoff}
    url = reverse("transactions_list")

    response = client.get(url, GET_params)

    qs = response.context["filter"].qs

    for transaction in qs:
        assert transaction.date <= end_date_cutoff


@pytest.mark.django_db
def test_category_filter(authenticate_user, client):
    cat_filter_no = 3
    category_pks = Category.objects.all()[:2].values_list(
        "pk",
        flat=True,
    )
    # GET_params = {"category": cat_filter_no}
    GET_params = {"category": category_pks}
    url = reverse("transactions_list")

    response = client.get(url, GET_params)

    qs = response.context["filter"].qs

    for transaction in qs:
        assert transaction.category.pk in category_pks
        # assert transaction.category.name == Category.objects.get(1
