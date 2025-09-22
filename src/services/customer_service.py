from typing import Dict, Optional, List
from src.dao.customer_dao import customer_dao
from src.dao.order_dao import order_dao

class CustomerError(Exception):
    pass

class CustomerService:
    def __init__(self, dao):
        self._dao = dao

    def add_customer(self, name: str, email: str, phone: str, city: Optional[str] = None) -> Dict:
        existing = self._dao.get_customer_by_email(email)
        if existing:
            raise CustomerError(f"Email already exists: {email}")
        return self._dao.create_customer(name, email, phone, city)

    def update_customer(self, cust_id: int, phone: Optional[str] = None, city: Optional[str] = None) -> Dict:
        customer = self._dao.get_customer_by_id(cust_id)
        if not customer:
            raise CustomerError("Customer not found")
        fields = {}
        if phone:
            fields["phone"] = phone
        if city:
            fields["city"] = city
        if not fields:
            raise CustomerError("No update fields provided")
        return self._dao.update_customer(cust_id, fields)

    def delete_customer(self, cust_id: int) -> Dict:
        orders = order_dao.get_orders_by_customer_id(cust_id)
        if orders:
            raise CustomerError("Cannot delete customer with existing orders")
        return self._dao.delete_customer(cust_id)

    def list_customers(self, limit: int = 100) -> List[Dict]:
        return self._dao.list_customers(limit)

    def search_customers(self, email: Optional[str] = None, city: Optional[str] = None) -> List[Dict]:
        if not email and not city:
            raise CustomerError("Provide at least email or city to search")
        return self._dao.search_customers(email, city)

customer_service = CustomerService(customer_dao)
