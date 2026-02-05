import unittest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

class TestAPI(unittest.TestCase):

    def test_unauthorized_get_usuarios(self):
        r = client.get("/usuarios")
        self.assertEqual(r.status_code, 401)  # HTTPBearer bloqueia sem token? (pode variar)

    def test_admin_list_usuarios(self):
        r = client.get("/usuarios", headers={"Authorization": "Bearer token-admin-123"})
        self.assertEqual(r.status_code, 200)

if __name__ == "__main__":
    unittest.main()
