from typing import List, Tuple
from itertools import combinations

import MyPac.MySubs3
import MyPac.MySubs2
import MyPac.MySubs6
import MyPac.MySubs9

def calc_risk_added_at_each_entry(str_arr_ents: List[str], no_of_entries: int, stop_loss: float, full_position_size: float, wanted_to_risk_amount: float) -> List[str]:
    total_risk_so_far = 0
    ret_arr = []

    for i in range(no_of_entries):
        splitter = str_arr_ents[i].split()
        entry_price = float(splitter[1])
        percentage = float(splitter[3].rstrip('%')) / 100

        entry_no = i + 1
        this_entry_position_size = full_position_size * percentage
        this_risked_percentage = abs(entry_price - stop_loss) / entry_price
        this_risked_amount = this_entry_position_size * this_risked_percentage * 100

        total_risk_so_far += this_risked_amount
        amount_still_left_to_risk = wanted_to_risk_amount - total_risk_so_far
        str1 = f"entry {entry_no}: riskAmountAddedHere=${this_risked_amount:.2f}, totRiskNow=${total_risk_so_far:.2f} " \
               f"(${wanted_to_risk_amount:.2f}-${total_risk_so_far:.2f}=${amount_still_left_to_risk:.2f} still to risk)"
        ret_arr.append(str1)

    return ret_arr

def heavy_weighting_at_entry_or_stop_loss(entries_or_targets_str: str, no_of_entries: int, high: float, low: float,
                                          is_trade_a_long: int, weighting_factor: float, no_decimal_places: int) -> List[str]:
    # Assuming MySubs2::EvenDistribution is implemented elsewhere
    str_arr = MyPac.MySubs2.even_distribution(entries_or_targets_str, no_of_entries, high, low, is_trade_a_long, no_decimal_places)

    percentages = [float(entry.split()[3].rstrip('%')) / 100 for entry in str_arr]
    arr_length_perc = len(percentages)
    is_even = arr_length_perc % 2 == 0
    temp = [i for i in range(arr_length_perc)]

    # Create an array of percentage "pairs" (next to each other in the array)
    temp_pairs = list(combinations(temp, 2) if is_even else combinations(temp[:-1], 2))

    for x in range(arr_length_perc // 2):
        for i in range(arr_length_perc // 2 - x):
            p = temp_pairs[i][1]
            percentages[i] -= weighting_factor
            percentages[p] += weighting_factor

    # Update str_arr with the new weighted percentages
    str_arr_new_percentages = [f"{entry.split()[0]} {entry.split()[1]} {entry.split()[2]} "
                               f"{MyPac.MySubs6.format_to_variable_number_of_decimal_places(percentages[i], 2)}%\n"
                               for i, entry in enumerate(str_arr)]

    return str_arr_new_percentages


def create_cornix_free_text_advanced_template(pair: str, client_selected: str, leverage: float, no_of_entries: int,
                                              high_entry: float, low_entry: float, no_of_targets: int, high_target: float,
                                              low_target: float, stop_loss: float, no_decimal_places: int,
                                              wanted_to_risk_amount: float, is_trade_a_long: int,
                                              weighting_factor_entries: float, weighting_factor_targets: float,
                                              dynamic_entry_value: float) -> List[str]:
    template = ["########################### advanced template", f"{pair}", f"Client: {client_selected}"]

    if is_trade_a_long == 1:
        template.append("Trade Type: Regular (Long)")
    elif is_trade_a_long == 0:
        template.append("Trade Type: Regular (Short)")
    else:
        raise ValueError("Cannot determine if trade is a long or a short for writing template")

    if leverage >= 1:
        template.append(f"Leverage: Cross ({leverage:.1f}X)")

    str_arr_entries = heavy_weighting_at_entry_or_stop_loss("entries", no_of_entries, high_entry, low_entry,
                                                            is_trade_a_long, weighting_factor_entries, no_decimal_places)
    template.extend(["", "Entry Targets:"] + str_arr_entries)

    str_arr_targets = heavy_weighting_at_entry_or_stop_loss("targets", no_of_targets, high_target, low_target,
                                                            is_trade_a_long, weighting_factor_targets, no_decimal_places)
    template.extend(["", "Take-Profit Targets:"] + str_arr_targets)

    sl = MyPac.MySubs6.format_to_variable_number_of_decimal_places(stop_loss, no_decimal_places)
    template.extend(["", f"Stop Targets:\n1) {sl} - 100%\n", ""])

    trailing_lines = [
        "Trailing Configuration:",
        "Entry: Percentage (0.0%)",
        "Take-Profit: Percentage (0.0%)",
        "Stop: Without"
    ]
    template.extend(trailing_lines)

    risk_soft_mult, risk_percentage_based_on_entry1, risk_percentage_based_on_avg_entry = MyPac.MySubs3.risk_softening_multiplier(
        str_arr_entries, stop_loss)

    position_size_entry1 = wanted_to_risk_amount / risk_percentage_based_on_entry1
    position_size_average_entry = wanted_to_risk_amount / risk_percentage_based_on_avg_entry

    dollars_risked_at_each_entry_ent1 = calc_risk_added_at_each_entry(str_arr_entries, no_of_entries, stop_loss,
                                                                      position_size_entry1,
                                                                      wanted_to_risk_amount * risk_soft_mult)
    dollars_risked_at_each_entry_avg_ent = calc_risk_added_at_each_entry(str_arr_entries, no_of_entries, stop_loss,
                                                                         position_size_average_entry,
                                                                         wanted_to_risk_amount)

    temp_arrays_concatenated_returned_from_sub = []
    frdps_data_ent1 = []
    frdps_data_avg_ent = []
    if dynamic_entry_value != 0:
        temp_arrays_concatenated_returned_from_sub = MyPac.MySubs9.fixed_risk_dynamic_position_size(str_arr_entries, stop_loss,
                                                                                        position_size_entry1,
                                                                                        position_size_average_entry,
                                                                                        wanted_to_risk_amount,
                                                                                        dynamic_entry_value,
                                                                                        is_trade_a_long)
        for i in range(no_of_entries):
            frdps_data_ent1.append(temp_arrays_concatenated_returned_from_sub[i])
            frdps_data_avg_ent.append(temp_arrays_concatenated_returned_from_sub[no_of_entries + i])

    temp_avg1 = "########################### risk based on average entry"
    temp_avg2 = f"riskPercentageBasedOnAvgEntry = {risk_percentage_based_on_avg_entry:.4f}"
    temp_avg3 = f"position size of ${position_size_average_entry:.2f} is needed to risk ${wanted_to_risk_amount:.2f}"
    template.extend([temp_avg1, temp_avg2, temp_avg3])

    for i in range(no_of_entries):
        template.append(dollars_risked_at_each_entry_avg_ent[i])

    if dynamic_entry_value != 0:
        template.append("\n########################### fixed risk dynamic position size")
        template.append("### only on entry 1")
        template.extend(frdps_data_ent1)
        template.append("### average entry")
        template.extend(frdps_data_avg_ent)

    return template

# The following functions are placeholders for functions not provided in the original code.

#def even_distribution(entries_or_targets_str: str, no_of_entries: int, high: float, low: float, is_trade_a_long: int,
#                      no_decimal_places: int) -> List[str]:
#    # Implement according to your requirements
#    pass

#def risk_softening_multiplier(str_arr_entries: List[str], stop_loss: float) -> Tuple[float, float, float]:
#    # Implement according to your requirements
#    pass

#def fixed_risk_dynamic_position_size(str_arr_entries: List[str], stop_loss: float, position_size_entry1: float,
#                                     position_size_average_entry: float, wanted_to_risk_amount: float,
#                                     dynamic_entry_value: float, is_trade_a_long: int) -> List[str]:
#    # Implement according to your requirements
#    pass

