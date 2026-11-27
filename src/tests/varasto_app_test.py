"""Tests for the warehouse web application."""

import json

import pytest

from varasto_app import WarehouseManager


def test_create_list_and_persist_warehouses(tmp_path):
    """Warehouses and their balances survive loading the saved file."""
    data_path = tmp_path / "data" / "warehouses.json"
    manager = WarehouseManager(data_path)
    warehouse = manager.create_warehouse("Main warehouse", 10)
    manager.change_balance(warehouse["id"], 4, adding=True)

    reloaded = WarehouseManager(data_path)

    assert reloaded.list_warehouses() == [
        {
            "id": warehouse["id"],
            "name": "Main warehouse",
            "capacity": 10,
            "balance": 4,
            "available": 6,
        }
    ]


def test_reject_invalid_warehouse_values(tmp_path):
    """Names and capacities must be usable and duplicate names are rejected."""
    manager = WarehouseManager(tmp_path / "warehouses.json")
    manager.create_warehouse("Main", 10)

    with pytest.raises(ValueError, match="name"):
        manager.create_warehouse("  ", 10)
    with pytest.raises(ValueError, match="greater than zero"):
        manager.create_warehouse("Small", 0)
    with pytest.raises(ValueError, match="already exists"):
        manager.create_warehouse("main", 20)


def test_stock_changes_obey_capacity_and_available_balance(tmp_path):
    """Stock additions cap at capacity and removals stop at zero."""
    manager = WarehouseManager(tmp_path / "warehouses.json")
    warehouse = manager.create_warehouse("Main", 10)

    full = manager.change_balance(warehouse["id"], 15, adding=True)
    empty = manager.change_balance(warehouse["id"], 15, adding=False)

    assert full["balance"] == 10
    assert full["available"] == 0
    assert empty["balance"] == 0
    assert empty["available"] == 10


def test_invalid_stock_changes_do_not_overwrite_data(tmp_path):
    """Invalid amounts and unknown warehouse IDs return clear errors."""
    data_path = tmp_path / "warehouses.json"
    manager = WarehouseManager(data_path)
    warehouse = manager.create_warehouse("Main", 10)
    saved_before = json.loads(data_path.read_text(encoding="utf-8"))

    with pytest.raises(ValueError, match="greater than zero"):
        manager.change_balance(warehouse["id"], -1, adding=True)
    with pytest.raises(KeyError, match="not found"):
        manager.change_balance("unknown", 1, adding=True)

    assert json.loads(data_path.read_text(encoding="utf-8")) == saved_before
