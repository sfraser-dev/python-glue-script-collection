from MySubs6 import HeavyWeightingAtEntryOrStoploss as weighting_at_entry_or_stoploss
from MySubs7 import formatToVariableNumberOfDecimalPlaces
from MySubs8 import calcRiskAddedAtEachEntry, fixedRiskDynamicPositionSize
from MySubs3 import riskSofteningMultiplier

def create_cornix_free_text_advanced_template(pair, client_selected, leverage, no_of_entries, high_entry, low_entry,
                                               no_of_targets, high_target, low_target, stop_loss,
                                               no_decimal_places_for_entries_targets_and_sls, wanted_to_risk_amount,
                                               is_trade_a_long, weighting_factor_entries, weighting_factor_targets,
                                               dynamic_entry_value):
    template = []
    str_read = ""
    risk_soft_mult = 0
    risk_percentage_based_on_entry1 = 0
    risk_percentage_based_on_avg_entry = 0

    template.append("########################### advanced template\n")

    # coin pairs
    template.append(f"{pair}\n")

    # Cornix client
    template.append(f"Client: {client_selected}\n")

    # long or short trade
    if is_trade_a_long == 1:
        template.append("Trade Type: Regular (Long)\n")
    elif is_trade_a_long == 0:
        template.append("Trade Type: Regular (Short)\n")
    else:
        raise ValueError("Error: cannot determine if trade is a long or a short for writing template")

    # amount of leverage to use (if any at all, "-1" means no leverage)
    if leverage >= 1:
        template.append(f"Leverage: Cross ({leverage}.0X)\n")

    # entry targets
    template.append("\n")
    template.append("Entry Targets:\n")
    str_arr_entries = weighting_at_entry_or_stoploss("entries", no_of_entries, high_entry, low_entry,
                                                     is_trade_a_long, weighting_factor_entries,
                                                     no_decimal_places_for_entries_targets_and_sls)
    template.extend(str_arr_entries)

    # take profit targets
    template.append("\n")
    template.append("Take-Profit Targets:\n")
    str_arr_targets = weighting_at_entry_or_stoploss("targets", no_of_targets, high_target, low_target,
                                                     is_trade_a_long, weighting_factor_targets,
                                                     no_decimal_places_for_entries_targets_and_sls)
    template.extend(str_arr_targets)

    # stop-loss
    sl = formatToVariableNumberOfDecimalPlaces(stop_loss, no_decimal_places_for_entries_targets_and_sls)
    template.append(f"\nStop Targets:\n1) {sl} - 100%\n\n")

    # trailing configuration
    trailing_line_01 = "Trailing Configuration:"
    trailing_line_02 = "Entry: Percentage (0.0%)"
    trailing_line_03 = "Take-Profit: Percentage (0.0%)"
    trailing_line_04 = "Stop: Without"
    template.append(f"{trailing_line_01}\n{trailing_line_02}\n{trailing_line_03}\n{trailing_line_04}\n\n")

    # risk softening multiplier (just for risk based on only entry1) and risk percentages
    (risk_soft_mult, risk_percentage_based_on_entry1, risk_percentage_based_on_avg_entry) = riskSofteningMultiplier(
        str_arr_entries, stop_loss)

    # position sizes required for the wanted risk (calc for both entry1 and average-entry)
    position_size_entry1 = wanted_to_risk_amount / risk_percentage_based_on_entry1
    position_size_average_entry = wanted_to_risk_amount / risk_percentage_based_on_avg_entry

    dollars_risked_at_each_entry_ent1 = calcRiskAddedAtEachEntry(str_arr_entries, no_of_entries, stop_loss,
                                                                 position_size_entry1, wanted_to_risk_amount * risk_soft_mult)
    dollars_risked_at_each_entry_avg_ent = calcRiskAddedAtEachEntry(str_arr_entries, no_of_entries, stop_loss,
                                                                    position_size_average_entry, wanted_to_risk_amount)

    # fixed risk dynamic position size calculation
    temp_arrays_concatenated_returned_from_sub = []
    frdps_data_ent1 = []
    frdps_data_avg_ent = []
    if dynamic_entry_value != 0:
        temp_arrays_concatenated_returned_from_sub = fixedRiskDynamicPositionSize(
            str_arr_entries, stop_loss, position_size_entry1, position_size_average_entry, wanted_to_risk_amount,
            dynamic_entry_value, is_trade_a_long)
        for i in range(no_of_entries):
            frdps_data_ent1.append(temp_arrays_concatenated_returned_from_sub[i])
            frdps_data_avg_ent.append(temp_arrays_concatenated_returned_from_sub[no_of_entries + i])

    # show position size needed for required risk percentage (based only on entry1)
    temp_ent1 = "########################### risk based only on entry 1\n"
    temp_ent2 = f"riskPercentageBasedOnEntry1 = {risk_percentage_based_on_entry1:.4f}\n"
    temp_ent3 = f"position size of ${position_size_entry1:.2f} is needed to risk ${wanted_to_risk_amount * risk_soft_mult:.2f}\n"
    template.extend([temp_ent1, temp_ent2, temp_ent3])
    # risk added at each entry (based only on entry1)
    for i in range(no_of_entries):
        str_entry = f"{dollars_risked_at_each_entry_ent1[i]}\n"
        template.append(str_entry)
    softened_risk = wanted_to_risk_amount * risk_soft_mult
    temp_ent6 = f"riskSoftMult: ${wanted_to_risk_amount:.2f} * {risk_soft_mult:.4f} = ${softened_risk:.2f}\n\n"
    template.append(temp_ent6)

    # show position size needed for required risk percentage (based average entry)
    temp_avg1 = "########################### risk based on average entry\n"
    temp_avg2 = f"riskPercentageBasedOnAvgEntry = {risk_percentage_based_on_avg_entry:.4f}\n"
    temp_avg3 = f"position size of ${position_size_average_entry:.2f} is needed to risk ${wanted_to_risk_amount:.2f}\n"
    template.extend([temp_avg1, temp_avg2, temp_avg3])
    # risk added at each entry (based only on avgEntry)
    for i in range(no_of_entries):
        str_avg_entry = f"{dollars_risked_at_each_entry_avg_ent[i]}\n"
        template.append(str_avg_entry)

    # Optional: show fixed risk dynamic position sizes
    if dynamic_entry_value != 0:
        # entry1
        template.append("\n########################### fixed risk dynamic position size\n")
        template.append("### only on entry 1\n")
        for i in range(no_of_entries):
            template.append(frdps_data_ent1[i])
        # average entry
        template.append("### average entry\n")
        for i in range(no_of_entries):
            template.append(frdps_data_avg_ent[i])

    return template


#if __name__ == "__main__":
#    # Example usage:
#    template_result = create_cornix_free_text_advanced_template("BTC/USD", "MyClient", 2
