"""
Test the views of the tracker app
"""

from django.urls import reverse
import pytest


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
