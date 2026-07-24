import unittest
from users import UserManager
from products import ProductManager
from orders import OrderManager
from payments import PaymentProcessor
from database import Database

class TestECommerce(unittest.TestCase):
    def setUp(self):
        self.db = Database("test.json")
        self.db.data = {"users": [], "products": [], "orders": [], "payments": []}
        self.user_manager = UserManager(self.db)
        self.product_manager = ProductManager(self.db)
        self.order_manager = OrderManager(self.db, self.user_manager, self.product_manager)
        self.payment_processor = PaymentProcessor(self.db)
    def test_user_creation(self):
        u = self.user_manager.create_user("akarsh", "akarsh@example.com")
        self.assertEqual(u.username, "akarsh")
    def test_product_addition(self):
        p = self.product_manager.add_product("Laptop", 75000, 10)
        self.assertEqual(p.name, "Laptop")
    def test_order_payment(self):
        u = self.user_manager.create_user("akarsh", "akarsh@example.com")
        p = self.product_manager.add_product("Phone", 35000, 5)
        o = self.order_manager.create_order(u.id, [p.id])
        pay = self.payment_processor.process_payment(o["id"], 35000)
        self.assertEqual(pay["status"], "Success")

if __name__ == "__main__":
    unittest.main()
