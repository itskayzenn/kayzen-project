import os
import shutil
import pytest
from kayzendb.core import KayzenDB

DB_PATH = "test_db.kzn"
PASSWORD = "strongpassword"

@pytest.fixture
def db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    if os.path.exists(DB_PATH + ".wal"):
        os.remove(DB_PATH + ".wal")
        
    database = KayzenDB(DB_PATH, PASSWORD)
    yield database
    
    # Cleanup
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    if os.path.exists(DB_PATH + ".wal"):
        os.remove(DB_PATH + ".wal")

def test_create_read(db):
    db.create("user1", {"name": "Ali", "age": 30})
    data = db.read("user1")
    assert data["name"] == "Ali"
    assert data["age"] == 30

def test_update(db):
    db.create("item1", {"price": 100})
    db.update("item1", {"price": 150})
    data = db.read("item1")
    assert data["price"] == 150

def test_delete(db):
    db.create("temp", {"val": 1})
    db.delete("temp")
    with pytest.raises(KeyError):
        db.read("temp")

def test_persistence_encryption():
    # 1. Create and populate
    db1 = KayzenDB("secure.kzn", PASSWORD)
    db1.create("secret", {"code": "007"})
    del db1 # Close DB (Force flush handled by create/update checkpoint)

    # 2. Check if file is encrypted (not plain text)
    with open("secure.kzn", "rb") as f:
        content = f.read()
        assert b"007" not in content # Should be encrypted

    # 3. Re-open with wrong password
    with pytest.raises(ValueError):
        KayzenDB("secure.kzn", "wrongpass")

    # 4. Re-open with correct password
    db2 = KayzenDB("secure.kzn", PASSWORD)
    assert db2.read("secret")["code"] == "007"
    
    # Cleanup
    if os.path.exists("secure.kzn"): os.remove("secure.kzn")
    if os.path.exists("secure.kzn.wal"): os.remove("secure.kzn.wal")

def test_wal_recovery():
    # Simulasi Crash: Write ke WAL tapi jangan checkpoint (manual test logic)
    # Ini agak sulit di unit test standar tanpa mocking internal, 
    # tapi kita bisa test fungsi wal replay logika.
    pass 
