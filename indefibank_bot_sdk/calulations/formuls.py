from decimal import Decimal


class IndefibankFormuls:
    @staticmethod
    def get_liquidity(price, collateral, debt_currency):
        """
            debt_currency = 100%
            collateral * price = x%
            x = (collateral * price * 100) / debt_currency
        """
        return round(((collateral * price * Decimal('100')) / debt_currency), 2)

    @staticmethod
    def get_liquidation_price(collateral, debt_currency, min_liquidity=150):
        """
            x * collateral * 100 = liquidity * debt_currency
            x = (liquidity * debt_currency) / (collateral * 100)
        """
        return round((min_liquidity * debt_currency) / (collateral * Decimal('100')), 2)

    @staticmethod
    def get_available_for_withdrawal_collateral(current_collateral_amount, price, min_liquidity, current_debt_currency_amount):
        """
            price * x * 100 = min_liquidity * current_debt_currency_amount
            x = (min_liquidity * current_debt_currency_amount) / (price * 100)

            available_for_withdrawal_collateral = current_collateral_amount - x
        """
        return round(current_collateral_amount - (min_liquidity * current_debt_currency_amount) / (price * Decimal('100')), 4)

    @staticmethod
    def get_available_for_generate_debt_currency(current_collateral_amount, price, min_liquidity, current_debt_currency_amount):
        """
            price * current_collateral_amount * 100 = liquidity * x
            x = (price * current_collateral_amount * 100) / min_liquidity

            available_for_generate_debt_currency = x - current_debt_currency_amount
        """
        return round((price * current_collateral_amount * Decimal('100')) / min_liquidity - current_debt_currency_amount, 2)

    @staticmethod
    def get_collateral_count(debt_amount, price, min_liquidity):
        """
            price * x * 100 = liquidity * debt_amount
            x = (liquidity * debt_amount) / (100 * price)
        """
        return round((debt_amount * min_liquidity) / (price * Decimal('100')), 2)
