"""Web application for managing warehouses."""

import json
import math
import re
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

from varasto import Varasto


class WarehouseManager:
    """Manage named warehouses and persist their balances as JSON."""

    def __init__(self, data_path="varastot.json"):
        self.data_path = Path(data_path)
        self.warehouses = {}
        self.lock = threading.RLock()
        self._load()

    def _load(self):
        if not self.data_path.exists():
            return

        with self.data_path.open(encoding="utf-8") as data_file:
            saved = json.load(data_file)

        for warehouse in saved:
            storage = Varasto(warehouse["capacity"], warehouse["balance"])
            self.warehouses[warehouse["id"]] = {
                "id": warehouse["id"],
                "name": warehouse["name"],
                "storage": storage,
            }

    @staticmethod
    def _number(value, label):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{label} must be a number")
        if not math.isfinite(value):
            raise ValueError(f"{label} must be finite")
        return float(value)

    def _serialize(self, warehouse):
        storage = warehouse["storage"]
        return {
            "id": warehouse["id"],
            "name": warehouse["name"],
            "capacity": storage.tilavuus,
            "balance": storage.saldo,
            "available": storage.paljonko_mahtuu(),
        }

    def list_warehouses(self):
        """Return all warehouses with their capacities and balances."""
        with self.lock:
            return [self._serialize(item) for item in self.warehouses.values()]

    def create_warehouse(self, name, capacity):  # pylint: disable=too-many-statements
        """Create a warehouse after validating its name and capacity."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Enter a warehouse name")
        name = name.strip()
        capacity = self._number(capacity, "Capacity")
        if capacity <= 0:
            raise ValueError("Capacity must be greater than zero")

        with self.lock:
            if any(item["name"].casefold() == name.casefold()
                   for item in self.warehouses.values()):
                raise ValueError("A warehouse with that name already exists")
            warehouse_id = str(uuid.uuid4())
            self.warehouses[warehouse_id] = {
                "id": warehouse_id,
                "name": name,
                "storage": Varasto(capacity),
            }
            self._save()
            return self._serialize(self.warehouses[warehouse_id])

    def change_balance(self, warehouse_id, amount, adding):  # pylint: disable=too-many-statements
        """Add or remove an amount, returning the updated warehouse."""
        amount = self._number(amount, "Amount")
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

        with self.lock:
            warehouse = self.warehouses.get(warehouse_id)
            if warehouse is None:
                raise KeyError("Warehouse not found")

            storage = warehouse["storage"]
            if adding:
                storage.lisaa_varastoon(amount)
            else:
                storage.ota_varastosta(amount)
            self._save()
            return self._serialize(warehouse)

    def _save(self):
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        saved = [
            {
                "id": item["id"],
                "name": item["name"],
                "capacity": item["storage"].tilavuus,
                "balance": item["storage"].saldo,
            }
            for item in self.warehouses.values()
        ]
        temporary_path = self.data_path.with_suffix(
            self.data_path.suffix + ".tmp"
        )
        with temporary_path.open("w", encoding="utf-8") as data_file:
            json.dump(saved, data_file, ensure_ascii=False, indent=2)
        temporary_path.replace(self.data_path)


def make_handler(manager):  # pylint: disable=too-many-statements
    """Create an HTTP handler connected to a warehouse manager."""

    class WarehouseHandler(BaseHTTPRequestHandler):
        """Serve the warehouse UI and its JSON API."""

        def _send_json(self, status, payload):
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _read_json(self):
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length <= 0 or length > 1_000_000:
                    raise ValueError("Invalid request size")
                return json.loads(self.rfile.read(length))
            except (ValueError, json.JSONDecodeError) as error:
                raise ValueError("Send a valid JSON request") from error

        def do_GET(self):  # pylint: disable=invalid-name, too-many-statements
            """Serve the UI and warehouse listing."""
            if self.path == "/api/warehouses":
                self._send_json(200, manager.list_warehouses())
                return
            if self.path in ("/", "/index.html"):
                page = Path(__file__).parent / "static" / "index.html"
                body = page.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            self._send_json(404, {"error": "Not found"})

        def do_POST(self):  # pylint: disable=invalid-name, too-many-statements
            """Handle warehouse creation and stock changes."""
            try:
                payload = self._read_json()
                if not isinstance(payload, dict):
                    raise ValueError("Send a JSON object")

                if self.path == "/api/warehouses":
                    result = manager.create_warehouse(
                        payload.get("name"), payload.get("capacity")
                    )
                    self._send_json(201, result)
                    return

                match = re.fullmatch(
                    r"/api/warehouses/([^/]+)/(add|remove)", self.path
                )
                if match:
                    warehouse_id = unquote(match.group(1))
                    result = manager.change_balance(
                        warehouse_id,
                        payload.get("amount"),
                        match.group(2) == "add",
                    )
                    self._send_json(200, result)
                    return
                self._send_json(404, {"error": "Not found"})
            except KeyError as error:
                self._send_json(404, {"error": str(error).strip("'")})
            except ValueError as error:
                self._send_json(400, {"error": str(error)})

        def log_message(self, format, *args):  # pylint: disable=unused-argument,redefined-builtin
            """Keep routine HTTP requests out of the terminal."""

    return WarehouseHandler


def main():
    """Start the warehouse application on localhost."""
    manager = WarehouseManager()
    server = ThreadingHTTPServer(("127.0.0.1", 8000), make_handler(manager))
    print("Warehouse app running at http://127.0.0.1:8000 (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping warehouse app")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
