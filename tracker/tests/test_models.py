"""
Test the models of tracker app
"""

import pytest
from tracker.models import Transaction


@pytest.mark.django_db
def test_manager_get_income_method(transactions):
    """
    Check whether get_income trx manager works correctly
    """
    # print(transactions.user, "trx_user")
    qs = Transaction.objects.get_income()

    assert qs.count() > 0
    assert all(
        [transactions.type == "income" for transactions in qs],
    )


@pytest.mark.django_db
def test_manager_get_expense_method(transactions):
    """
    Check whether get_income trx manager works correctly
    """
    qs = Transaction.objects.get_expenses()

    assert qs.count() > 0
    assert all(
        [transaction.type == "expense" for transaction in qs],
    )


@pytest.mark.django_db
def test_manager_get_total_income_method(transactions):
    """
    Tests whether the trx manager gets the total income
    """
    total_income = Transaction.objects.get_total_income()

    assert total_income == sum(t.amount for t in transactions if t.type == "income")


@pytest.mark.django_db
def test_manager_get_total_expense_method(transactions):
    """
    Tests whether the manager gets the total expenditure
    """
    total_expenses = Transaction.objects.get_total_expenses()

    assert total_expenses == sum(t.amount for t in transactions if t.type == "expense")
