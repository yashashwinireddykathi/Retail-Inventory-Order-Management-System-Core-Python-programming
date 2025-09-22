from typing import List, Dict, Optional
from src.config import get_supabase

class OrderDAO:
    def __init__(self):
        self._client = get_supabase()

    def _table(self):
        return self._client.table("orders")

    def create_order(self, cust_id: int, total_amount: float, status: str = "PLACED") -> Optional[Dict]:
        payload = {
            "cust_id": cust_id,
            "total_amount": total_amount,
            "status": status
        }
        self._table().insert(payload).execute()
        resp = self._table().select("*").eq("cust_id", cust_id).order("order_id", desc=True).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_orders_by_customer_id(self, cust_id: int) -> List[Dict]:
        resp = self._table().select("*").eq("cust_id", cust_id).execute()
        return resp.data or []

    def list_orders(self, limit: int = 100) -> List[Dict]:
        resp = self._table().select("*").order("order_date", desc=True).limit(limit).execute()
        return resp.data or []

order_dao = OrderDAO()
