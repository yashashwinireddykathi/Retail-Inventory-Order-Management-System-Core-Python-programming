import argparse
import json
from src.services.product_service import product_service
from src.dao.product_dao import product_dao
from src.services.customer_service import customer_service
from src.dao.customer_dao import customer_dao
from src.services.order_service import order_service

class RetailCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="retail-cli")
        self.sub = self.parser.add_subparsers(dest="cmd")
        self._setup_product_commands()
        self._setup_customer_commands()
        self._setup_order_commands()

    def _setup_product_commands(self):
        p_prod = self.sub.add_parser("product", help="product commands")
        pprod_sub = p_prod.add_subparsers(dest="action")

        addp = pprod_sub.add_parser("add")
        addp.add_argument("--name", required=True)
        addp.add_argument("--sku", required=True)
        addp.add_argument("--price", type=float, required=True)
        addp.add_argument("--stock", type=int, default=0)
        addp.add_argument("--category", default=None)
        addp.set_defaults(func=self._cmd_product_add)

        listp = pprod_sub.add_parser("list")
        listp.set_defaults(func=self._cmd_product_list)

    def _setup_customer_commands(self):
        p_cust = self.sub.add_parser("customer", help="customer commands")
        pcust_sub = p_cust.add_subparsers(dest="action")

        addc = pcust_sub.add_parser("add")
        addc.add_argument("--name", required=True)
        addc.add_argument("--email", required=True)
        addc.add_argument("--phone", required=True)
        addc.add_argument("--city", default=None)
        addc.set_defaults(func=self._cmd_customer_add)

        updatec = pcust_sub.add_parser("update")
        updatec.add_argument("--id", type=int, required=True, help="Customer ID")
        updatec.add_argument("--phone", default=None)
        updatec.add_argument("--city", default=None)
        updatec.set_defaults(func=self._cmd_customer_update)

        deletec = pcust_sub.add_parser("delete")
        deletec.add_argument("--id", type=int, required=True)
        deletec.set_defaults(func=self._cmd_customer_delete)

        listc = pcust_sub.add_parser("list")
        listc.set_defaults(func=self._cmd_customer_list)

        searchc = pcust_sub.add_parser("search")
        searchc.add_argument("--email", default=None)
        searchc.add_argument("--city", default=None)
        searchc.set_defaults(func=self._cmd_customer_search)

    def _setup_order_commands(self):
        p_order = self.sub.add_parser("order", help="order commands")
        porder_sub = p_order.add_subparsers(dest="action")

        addo = porder_sub.add_parser("add")
        addo.add_argument("--cust_id", type=int, required=True)
        addo.add_argument("--total_amount", type=float, required=True)
        addo.add_argument("--status", default="PLACED")
        addo.set_defaults(func=self._cmd_order_add)

        listo = porder_sub.add_parser("list")
        listo.set_defaults(func=self._cmd_order_list)

    # Product handlers
    def _cmd_product_add(self, args):
        try:
            product = product_service.add_product(
                name=args.name,
                sku=args.sku,
                price=args.price,
                stock=args.stock,
                category=args.category
            )
            print("Created product:")
            print(json.dumps(product, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def _cmd_product_list(self, args):
        try:
            products = product_dao.list_products(limit=100)
            print(json.dumps(products, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    # Customer handlers
    def _cmd_customer_add(self, args):
        try:
            customer = customer_service.add_customer(
                name=args.name,
                email=args.email,
                phone=args.phone,
                city=args.city
            )
            print("Created customer:")
            print(json.dumps(customer, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def _cmd_customer_update(self, args):
        try:
            customer = customer_service.update_customer(
                cust_id=args.id,
                phone=args.phone,
                city=args.city
            )
            print("Updated customer:")
            print(json.dumps(customer, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def _cmd_customer_delete(self, args):
        try:
            deleted = customer_service.delete_customer(args.id)
            print("Deleted customer:")
            print(json.dumps(deleted, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def _cmd_customer_list(self, args):
        try:
            customers = customer_dao.list_customers(limit=100)
            print(json.dumps(customers, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def _cmd_customer_search(self, args):
        try:
            customers = customer_service.search_customers(email=args.email, city=args.city)
            print(json.dumps(customers, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    # Order handlers
    def _cmd_order_add(self, args):
        try:
            order = order_service.create_order(
                cust_id=args.cust_id,
                total_amount=args.total_amount,
                status=args.status
            )
            print("Created order:")
            print(json.dumps(order, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def _cmd_order_list(self, args):
        try:
            orders = order_service.list_orders(limit=100)
            print(json.dumps(orders, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def run(self):
        args = self.parser.parse_args()
        if not hasattr(args, "func"):
            self.parser.print_help()
            return
        args.func(args)

if __name__ == "__main__":
    cli = RetailCLI()
    cli.run()
