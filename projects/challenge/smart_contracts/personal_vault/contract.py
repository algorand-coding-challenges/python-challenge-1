from algopy import (
    ARC4Contract,
    UInt64,
    arc4,
    itxn,
    Global,
    LocalState,
    Txn,
    gtxn,
    op,
)

class PersonalVault(ARC4Contract):
    def __init__(self) -> None:
        self.balance = LocalState(UInt64)

    @arc4.baremethod(allow_actions=["OptIn"])
    def opt_in_to_app(self) -> None:
        self.balance[Txn.sender] = UInt64(0)

    @arc4.abimethod()
    def deposit(self, ptxn: gtxn.PaymentTransaction) -> UInt64:
        assert ptxn.amount > 0, "Deposit amount must be greater than 0"
        
        # Corrected the receiver check
        assert (
            ptxn.receiver == Global.current_application_address
        ), "Deposit receiver must be the contract address"

        assert ptxn.sender == Txn.sender, "Deposit sender must be the caller"
        
        # Corrected the argument type for app_opted_in
        assert op.app_opted_in(
            Txn.sender, Global.current_application_id
        ), "Deposit sender must opt-in to the app first."

        self.balance[Txn.sender] += ptxn.amount
        user_balance = self.balance[Txn.sender]

        return user_balance

    @arc4.abimethod(allow_actions=["CloseOut"])
    def withdraw(self) -> UInt64:
        user_balance = self.balance[Txn.sender]

        itxn.Payment(
            receiver=Txn.sender,
            sender=Global.current_application_address,
            amount=user_balance,
            fee=0,
        ).submit()

        return user_balance
