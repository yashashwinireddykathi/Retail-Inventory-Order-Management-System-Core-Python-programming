from typing import Optional, List, Dict
from src.config import get_supabase

class ProductDAO:
    """
    OOP Data Access Object for 'products' table
    """

    def __init__(self):
        self._client = get_supabase()  # Encapsulated Supabase client

    # Internal table accessor
    def _table(self):
        return self._client.table("products")

    # Create product
    def create_product(
        self, name: str, sku: str, price: float, stock: int = 0, category: Optional[str] = None
    ) -> Optional[Dict]:
        payload = {"name": name, "sku": sku, "price": price, "stock": stock}
        if category:
            payload["category"] = category
        self._table().insert(payload).execute()
        resp = self._table().select("*").eq("sku", sku).limit(1).execute()
        return resp.data[0] if resp.data else None

    # Get product by ID
    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        resp = self._table().select("*").eq("product_id", product_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    # Get product by SKU
    def get_product_by_sku(self, sku: str) -> Optional[Dict]:
        resp = self._table().select("*").eq("sku", sku).limit(1).execute()
        return resp.data[0] if resp.data else None

    # Update product
    def update_product(self, product_id: int, fields: Dict) -> Optional[Dict]:
        self._table().update(fields).eq("product_id", product_id).execute()
        resp = self._table().select("*").eq("product_id", product_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    # Delete product
    def delete_product(self, product_id: int) -> Optional[Dict]:
        resp_before = self._table().select("*").eq("product_id", product_id).limit(1).execute()
        row = resp_before.data[0] if resp_before.data else None
        self._table().delete().eq("product_id", product_id).execute()
        return row

    # List products
    def list_products(self, limit: int = 100, category: Optional[str] = None) -> List[Dict]:
        q = self._table().select("*").order("product_id", desc=False).limit(limit)
        if category:
            q = q.eq("category", category)
        resp = q.execute()
        return resp.data or []

# Create the DAO object to use throughout the project
product_dao = ProductDAO()
