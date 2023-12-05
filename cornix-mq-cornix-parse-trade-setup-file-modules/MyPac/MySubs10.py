import os

def read_trade_config_file(path_to_file):
    data_hash = {
        'coinPair': "xxx/usdt",
        'client': 999999,
        'leverage': 999999,
        'numberOfEntries': 0,
        'highEntry': 0,
        'lowEntry': 0,
        'stopLoss': 0,
        'numberOfTargets': 0,
        'lowTarget': 0,
        'highTarget': 0,
        'noDecimalPlacesForEntriesTargetsAndSLs': 0,
        'wantedToRiskAmount': 999999
    }

    with open(path_to_file, 'r') as info:
        for line in info:
            line = line.strip()

            if line.startswith('#'):  # Skip comments
                continue

            if 'coinPair' in line:
                data_hash['coinPair'] = line.split('=')[1].strip()
            elif 'client' in line:
                data_hash['client'] = int(line.split('=')[1].strip())
            elif 'leverage' in line:
                leverage = int(line.split('=')[1].strip())
                data_hash['leverage'] = leverage if leverage >= 1 else 0
            elif 'numberOfEntries' in line:
                data_hash['numberOfEntries'] = int(line.split('=')[1].strip())
            elif 'highEntry' in line:
                data_hash['highEntry'] = float(line.split('=')[1].strip())
            elif 'lowEntry' in line:
                data_hash['lowEntry'] = float(line.split('=')[1].strip())
            elif 'stopLoss' in line:
                data_hash['stopLoss'] = float(line.split('=')[1].strip())
            elif 'numberOfTargets' in line:
                data_hash['numberOfTargets'] = int(line.split('=')[1].strip())
            elif 'lowTarget' in line:
                data_hash['lowTarget'] = float(line.split('=')[1].strip())
            elif 'highTarget' in line:
                data_hash['highTarget'] = float(line.split('=')[1].strip())
            elif 'numDecimalPlacesForCoinPrices' in line:
                data_hash['noDecimalPlacesForEntriesTargetsAndSLs'] = int(line.split('=')[1].strip())
            elif 'wantedToRiskAmount' in line:
                data_hash['wantedToRiskAmount'] = float(line.split('=')[1].strip())

    return data_hash

