import pytest
from app.calculations import add, substract, multiply, divide, BankAccount, Insufficient_balance

# Fixtures for class BankAccount
@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

# For Functions
@pytest.mark.parametrize("num1, num2, result", [
    (3, 2, 5),
    (7, 1, 8),
    (11, 11, 22)
])
def test_add(num1, num2, result):
    assert add(num1,num2) == result
    
def test_substract():
    assert substract(8,3) == 5
    
def test_multiply():
    assert multiply(11,11) == 121
    
def test_divide():
    assert divide(6,2) == 3
    
# For Classes
def test_bank_set_init_amount(bank_account):
    # bank_account = BankAccount(50)
    assert bank_account.balance == 50 
    
def test_bank_set_default_amount(zero_bank_account):
    # bank_account = BankAccount()
    assert zero_bank_account.balance == 0 
    
def test_withdraw(bank_account):
    # bank_account = BankAccount(50)
    bank_account.withdraw(20) 
    assert bank_account.balance == 30
    
def test_deposit(bank_account):
    # bank_account = BankAccount(50)
    bank_account.deposit(30)
    assert bank_account.balance == 80
    
def test_collect_interest(bank_account):
    # bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance, 6)  == 55
    
@pytest.mark.parametrize("deposited, withdraw, balance", [
    (2000, 1000, 1000),
    (50000, 25000, 25000),
])
def test_bank_transaction(zero_bank_account, deposited, withdraw, balance):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == balance
    
def test_insufficient_balance(bank_account):
    with pytest.raises(Insufficient_balance):
        bank_account.withdraw(200)

