from codility_fiddle_2 import DatabaseSimulator
import pytest

def test_multiple_keys():
    db = DatabaseSimulator()
    begin = db.begin() # begins a transaction
    assert begin == None

    geta = db.get("a") # returns None
    assert geta == None

    seta = db.set("a", "Hello A")
    assert seta == None

    geta2 = db.get("a") # returns 'Hello'
    assert geta2 == 'Hello A'
    
    setb = db.set("b", "Hello B")
    assert setb == None

    count = db.count() # returns 0
    assert count == 0
    
    commit = db.commit()
    assert commit == None
    
    geta3 = db.get("a") # returns 'Hello A'
    assert geta3 == 'Hello A'

    getb = db.get("b") # returns 'Hello B'
    assert getb == 'Hello B'

    count2 = db.count() # returns 2
    assert count2 == 2

def test_no_active_transaction():
    db = DatabaseSimulator()
    
    # Test get with no active transaction
    assert db.get("b") is None  # returns None
    
    # Test count with no active transaction
    assert db.count() == 0  # returns 0
    
    # Test set with no active transaction
    with pytest.raises(Exception, match="No active transaction"):
        db.set("b", "Hello")  # throws error "No active transaction"
    
    # Test commit with no active transaction
    with pytest.raises(Exception, match="No active transaction"):
        db.commit()  # throws error "No active transaction"
    
    # Test rollback with no active transaction
    with pytest.raises(Exception, match="No active transaction"):
        db.rollback()  # throws error "No active transaction"

def test_rollbacking():
    db = DatabaseSimulator()
    
    # Begin a transaction
    begin = db.begin()
    assert begin is None  # begins a transaction
    
    # Set key "a" to "Hello"
    seta1 = db.set("a", "Hello")
    assert seta1 is None
    
    # Update key "a" to "Hello world"
    seta2 = db.set("a", "Hello world")
    assert seta2 is None
    
    # Get key "a" should return "Hello world"
    geta = db.get("a")
    assert geta == "Hello world"  # returns 'Hello world'
    
    # Rollback the transaction
    rollback = db.rollback()
    assert rollback is None
    
    # Get key "a" should return None after rollback
    geta_after_rollback = db.get("a")
    assert geta_after_rollback is None  # returns None
    
    # Count should return 0 after rollback
    count = db.count()
    assert count == 0  # returns 0

def test_nested_transactions():
    db = DatabaseSimulator()
    
    # Begin the first transaction
    begin1 = db.begin()
    assert begin1 is None  # begins a transaction
    
    # Set key "a" to "Hello"
    seta1 = db.set("a", "Hello")
    assert seta1 is None
    
    # Begin the second transaction
    begin2 = db.begin()
    assert begin2 is None  # begins another transaction
    
    # Update key "a" to "Hello World"
    seta2 = db.set("a", "Hello World")
    assert seta2 is None
    
    # Get key "a" should return "Hello World"
    geta = db.get("a")
    assert geta == "Hello World"  # returns 'Hello World'
    
    # Commit the second transaction
    commit = db.commit()
    assert commit is None
    
    # Get key "a" should still return "Hello World" after commit
    geta_after_commit = db.get("a")
    assert geta_after_commit == "Hello World"  # returns 'Hello World'
    
    # Count should return 1 after commit
    count = db.count()
    assert count == 1  # returns 1

def test_nested_transactions_with_rollback():
    db = DatabaseSimulator()
    
    # Begin the first transaction
    begin1 = db.begin()
    assert begin1 is None  # begins a transaction
    
    # Set key "a" to "Hello"
    seta1 = db.set("a", "Hello")
    assert seta1 is None
    
    # Begin the second transaction
    begin2 = db.begin()
    assert begin2 is None  # begins another transaction
    
    # Update key "a" to "Hello World"
    seta2 = db.set("a", "Hello World")
    assert seta2 is None
    
    # Set key "b" to "Hello"
    setb = db.set("b", "Hello")
    assert setb is None
    
    # Rollback the second transaction
    rollback = db.rollback()
    assert rollback is None
    
    # Get key "a" should return "Hello" after rollback
    geta_after_rollback = db.get("a")
    assert geta_after_rollback == "Hello"  # returns 'Hello'
    
    # Get key "b" should return None after rollback
    getb_after_rollback = db.get("b")
    assert getb_after_rollback is None  # returns None
    
    # Commit the first transaction
    commit = db.commit()
    assert commit is None
    
    # Count should return 1 after commit
    count = db.count()
    assert count == 1  # returns 1