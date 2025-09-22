from src.dao.order_dao import order_dao

class OrderService:
    def __init__(self, dao):
        self._dao = dao

    def create_order(self, cust_id: int, total_amount: float, status: str = "PLACED"):
        return self._dao.create_order(cust_id, total_amount, status)

    def get_orders_by_customer_id(self, cust_id: int):
        return self._dao.get_orders_by_customer_id(cust_id)

    def has_orders(self, cust_id: int) -> bool:
        orders = self.get_orders_by_customer_id(cust_id)
        return len(orders) > 0

    def list_orders(self, limit: int = 100):
        return self._dao.list_orders(limit)

order_service = OrderService(order_dao)
