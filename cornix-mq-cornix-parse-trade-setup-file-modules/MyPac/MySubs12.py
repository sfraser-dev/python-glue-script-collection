def get_cornix_client_name(client_num):
    client_name_map = {
        1: "BM BinFuts (main)",
        2: "BM BinSpot (main)",
        3: "BM BybitKB7 Contract InvUSD (main) 260321",
        4: "BM BybitKB7 Contract LinUSDT (main) 211128",
        5: "SF BinFuts (main)",
        6: "SF BinSpot (main)",
        7: "SF Bybit Contract InvUSD (main) 210318",
        8: "BM BybitKB7 Contract LinUSDT (main) 281121",
        9: "SF FtxFuturesPerp (main)",
        10: "SF FtxFSpot (main)",
        11: "SF KucoinSpot (main)",
        12: "SF Bybit Contract LinUSDT (main) 281121",
    }

    if client_num not in client_name_map:
        raise Exception("error: can't determine Cornix client/exchange name")

    return client_name_map[client_num]

