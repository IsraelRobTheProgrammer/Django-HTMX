from django.db import models


class TrxQuerySet(models.QuerySet):
    def get_expenses(self):
        """Get transactions with type expenses"""
        return self.filter(type="expense")

    def get_income(self):
        """Get transactions with type income"""
        return self.filter(type="income")

    def get_total_expenses(self):
        """
        Get sum total of transactions with type expenses
        """
        return (
            self.get_expenses().aggregate(
                total=models.Sum(
                    "amount",
                )
            )["total"]
            or 0
        )

    def get_total_income(self):
        """
        Get sum total of transactions with type income
        """
        return (
            self.get_income().aggregate(
                total=models.Sum(
                    "amount",
                )
            )["total"]
            or 0
        )
