import logging

import algokit_utils
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from algosdk.transaction import *

from algokit_utils import EnsureBalanceParameters, TransactionParameters
from algosdk.atomic_transaction_composer import (
    TransactionWithSigner,
)

logger = logging.getLogger(__name__)


# define deployment behaviour based on supplied app spec
def deploy(
    algod_client: AlgodClient,
    indexer_client: IndexerClient,
    app_spec: algokit_utils.ApplicationSpecification,
    deployer: algokit_utils.Account,
) -> None:
    from smart_contracts.artifacts.personal_vault.client import (
        PersonalVaultClient,
    )

    # 1. Instantiate the app client. Used for deploying and interacting with the app.
    app_client = PersonalVaultClient(
        algod_client,
        creator=deployer,
        indexer_client=indexer_client,
    )

    # 2. Deploy the app to Algorand local blockchain.
    app_client.app_client.create()
    logger.info(f"Created App ID: {app_client.app_id}")

    # 3. Fund the app to cover Minimum Balance Requirement (https://developer.algorand.org/docs/get-details/dapps/smart-contracts/apps/?from_query=minimum#minimum-balance-requirement-for-a-smart-contract)
    algokit_utils.ensure_funded(
        algod_client,
        EnsureBalanceParameters(
            account_to_fund=app_client.app_address,
            min_spending_balance_micro_algos=0,
        ),
    )

    # 4. Create payment transaction object of 1000000 microAlgos (1 ALGO) to deposit funds to the app.
    sp = algod_client.suggested_params()
    ptxn = PaymentTxn(
        sender=deployer.address, sp=sp, receiver=app_client.app_address, amt=1000000
    )

    # 5. Create a transaction with the signer so the app client knows who is signing the payment txn.
    ptxn_with_signer = TransactionWithSigner(ptxn, deployer.signer)

    """
    # 6. Atomically group the payment transaction, app opt-in transaction, and the deposit method call transaction and execute them simultaneously.

    Why do we need to atomically group the 3 transactions?
    - payment txn: Algorand smart contracts are not accounts so need to send the payment to the associated contract account.
    - app opt-in txn: The depositor needs to opt-in to the contract so that the contract can create a local state for the depositor.
    - deposit method call txn: Contract method call to deposit funds to the contract.
    """
    response = (
        app_client.compose().opt_in_bare().deposit(ptxn=ptxn_with_signer).execute()
    )
    depositResponse = response.abi_results[0]

    logger.info(
        f"Deposited {(depositResponse.return_value) // 1000000} Algo to the bank contract in transaction {depositResponse.tx_id}."
    )

    # 7. Depositor withdraw funds from the contract.
    sp = algod_client.suggested_params()
    sp.flat_fee = True
    sp.fee = 2000  # doubling the base txn fee to cover the inner transaction fee of the withdraw method call.

    response = app_client.close_out_withdraw(
        transaction_parameters=TransactionParameters(suggested_params=sp)
    )

    logger.info(
        f"User withdrew {response.return_value // 1000000 } Algo from the bank contract in transaction {response.tx_id}."
    )
