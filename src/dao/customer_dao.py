from typing import Dict, Optional, List
from src.config import get_supabase

class CustomerDAO:
    def __init__(self):
        self._client = get_supabase()

    def _table(self):
        return self._client.table("customers")

    def create_customer(self, name: str, email: str, phone: str, city: Optional[str] = None) -> Optional[Dict]:
        payload = {"name": name, "email": email, "phone": phone}
        if city:
            payload["city"] = city
        self._table().insert(payload).execute()
        resp = self._table().select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_customer_by_id(self, cust_id: int) -> Optional[Dict]:
        resp = self._table().select("*").eq("cust_id", cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_customer_by_email(self, email: str) -> Optional[Dict]:
        resp = self._table().select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None

    def update_customer(self, cust_id: int, fields: Dict) -> Optional[Dict]:
        self._table().update(fields).eq("cust_id", cust_id).execute()
        resp = self._table().select("*").eq("cust_id", cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def delete_customer(self, cust_id: int) -> Optional[Dict]:
        resp_before = self._table().select("*").eq("cust_id", cust_id).limit(1).execute()
        row = resp_before.data[0] if resp_before.data else None
        self._table().delete().eq("cust_id", cust_id).execute()
        return row

    def list_customers(self, limit: int = 100) -> List[Dict]:
        resp = self._table().select("*").order("cust_id", desc=False).limit(limit).execute()
        return resp.data or []

    def search_customers(self, email: Optional[str], city: Optional[str]) -> List[Dict]:
        q = self._table().select("*")
        if email:
            q = q.ilike("email", f"%{email}%")
        if city:
            q = q.ilike("city", f"%{city}%")
        resp = q.execute()
        return resp.data or []

customer_dao = CustomerDAO()
