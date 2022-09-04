from web3 import Web3
from web3.middleware import geth_poa_middleware
from loguru import logger
from sys import stderr
from multiprocessing.dummy import Pool

logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white>"
                          " | <level>{level: <8}</level>"
                          " | <cyan>{line}</cyan>"
                          " - <white>{message}</white>")


def send_tx(private_key: str):
    address = None

    try:
        address = Web3.toChecksumAddress(w3.eth.account.from_key(private_key).address)
        transaction = contract.functions.buy(500,
                                             '0xB8B1E2665138aB79BF2ed11828009d4Ee4c32036') \
            .buildTransaction({
                'gas': 354853,
                'value': w3.toWei(0.5, 'ether'),
                'gasPrice': Web3.toWei(gwei, 'gwei'),
                'from': address,
                'nonce': w3.eth.getTransactionCount(address)
            })

        while w3.eth.get_block('latest')['timestamp']+time_median < START_SALE:
            pass

        signed_txn = w3.eth.account.signTransaction(transaction,
                                                    private_key=private_key)
        w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        tx_hash = w3.toHex(w3.keccak(signed_txn.rawTransaction))

        logger.info(f'{address} | {tx_hash}')

    except Exception as error:
        logger.error(f'{address} | {error}')


if __name__ == '__main__':
    START_SALE = 1662325199

    with open('accounts.txt', encoding='utf-8-sig') as file:
        private_keys = [row.strip() for row in file]

    with open('ABI', 'r', encoding='utf-8-sig') as file:
        ABI = file.read().strip().replace('\n', '').replace(' ', '')

    w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed2.binance.org/'))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    contract = w3.eth.contract(address=Web3.toChecksumAddress('0xa1b941c10c24338b5caafd90d083bf679c453218'),
                               abi=ABI)

    logger.info(f'Загружено {len(private_keys)} кошельков')

    time_median = int(input('За сколько секунд до сейла отправить TX: '))
    gwei = int(input('GWEI: '))

    with Pool(processes=len(private_keys)) as executor:
        executor.map(send_tx, private_keys)

    input('Press Enter To Exit..')
