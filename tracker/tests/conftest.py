import pytest
from tracker.factories import TransactionFactory, UserFactory


@pytest.fixture
def transactions():
    """return a batch of transactions"""
    return TransactionFactory.create_batch(20)


@pytest.fixture
def user_transactions():
    user = UserFactory()
    return TransactionFactory.create_batch(20, user=user)


@pytest.fixture
def authenticate_user(user_transactions, client):
    user = user_transactions[0].user
    logged_user = client.force_login(user)
    return logged_user
