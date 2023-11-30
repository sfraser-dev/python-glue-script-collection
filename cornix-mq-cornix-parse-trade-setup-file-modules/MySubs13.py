def check_values_from_config_file(noOfEntries, noOfTargets, highEntry, lowEntry, highTarget, lowTarget, stopLoss, leverage, noDecimalPlacesForEntriesTargetsAndSLs, wantedToRiskAmount):
    # Number of entries validation
    if noOfEntries < 1 or noOfEntries > 10:
        raise Exception("error: noOfEntries should be between 1 and 10 inclusive")

    # Number of targets validation
    if noOfTargets < 1 or noOfTargets > 10:
        raise Exception("error: noOfTargets should be between 1 and 10 inclusive")

    # High entry validation
    if highEntry <= lowEntry:
        raise Exception("error: highEntry must be greater than lowEntry")

    # High target validation
    if highTarget <= lowTarget:
        raise Exception("error: highTarget must be greater than lowTarget")

    # Determine trade type (long or short)
    isTradeALong = None
    if (highEntry > highTarget) and (highEntry > lowTarget) and (lowEntry > highTarget) and (lowEntry > lowTarget):
        isTradeALong = 0
    elif (highEntry < highTarget) and (highEntry < lowTarget) and (lowEntry < highTarget) and (lowEntry < lowTarget):
        isTradeALong = 1
    else:
        raise Exception("error: TradeType must be 'long' or 'short'")

    # Check stop-loss placement
    if isTradeALong == 1 and stopLoss >= lowEntry:
        raise Exception("error: wrong stop-loss placement for a long trade")
    elif isTradeALong == 0 and stopLoss <= highEntry:
        raise Exception("error: wrong stop-loss placement for a short trade")

    # Leverage validation
    if leverage < -1 or leverage > 20:
        raise Exception("error: incorrect leverage (-1 <= leverage <= 20)")

    # Decimal places validation
    if noDecimalPlacesForEntriesTargetsAndSLs < 0 or noDecimalPlacesForEntriesTargetsAndSLs > 10:
        raise Exception("error: invalid number of decimal places for entries and targets")

    # Risked amount validation
    if wantedToRiskAmount <= 0:
        raise Exception("error: wantedToRiskAmount must be greater than 0")

    return isTradeALong

