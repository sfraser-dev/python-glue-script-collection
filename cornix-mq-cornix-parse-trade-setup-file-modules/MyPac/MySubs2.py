import MySubs5.format_to_variable_number_of_decimal_places

def even_distribution(entries_or_targets, no_of_entries_or_targets_wanted, high, low, is_trade_a_long, no_decimal_places):
    str_arr = []

    # Handle a single entry
    if no_of_entries_or_targets_wanted == 1:
        str_arr.append("1) {} - 100%\n".format(format_to_variable_number_of_decimal_places(high, no_decimal_places)))
        return str_arr

    # Calculate entry/target values based on high, low, and number of entries
    high_low_diff = high - low
    entry_increment = high_low_diff / (no_of_entries_or_targets_wanted - 1)

    entry_or_target_vals_arr = []

    # Place entries or targets in the correct order based on long or short trade
    if entries_or_targets == "entries":
        # Long entries (high to low)
        if is_trade_a_long:
            for i in range(no_of_entries_or_targets_wanted):
                entry_or_target_vals_arr.append(high - (entry_increment * i))
        # Short entries (low to high)
        elif not is_trade_a_long:
            for i in range(no_of_entries_or_targets_wanted):
                entry_or_target_vals_arr.append(low + (entry_increment * i))
        else:
            raise Exception("Error: Trade must be declared as long or short when generating entries")
    elif entries_or_targets == "targets":
        # Long targets (low to high)
        if is_trade_a_long:
            for i in range(no_of_entries_or_targets_wanted):
                entry_or_target_vals_arr.append(low + (entry_increment * i))
        # Short targets (high to low)
        elif not is_trade_a_long:
            for i in range(no_of_entries_or_targets_wanted):
                entry_or_target_vals_arr.append(high - (entry_increment * i))
        else:
            raise Exception("Error: Trade must be declared as long or short when generating targets")
    else:
        raise Exception("Error: Must declare whether generating entries or targets")

    # Calculate percentage values
    percentage_increment = 100 / no_of_entries_or_targets_wanted

    # Round percentage values to integers
    percent_increment_base = int(percentage_increment)
    percentage_arr = []
    sum_ = 0
    for i in range(no_of_entries_or_targets_wanted):
        percentage_arr.append(percent_increment_base)
        sum_ += percent_increment_base

    # Adjust percentages to total 100
    if sum_ < 100:
        to_add = 100 - sum_
        array_size = len(percentage_arr)
        for i in range(to_add):
            percentage_arr[i] += 1

    # Print out entries/targets and their percentage allocations
    for i, val in enumerate(entry_or_target_vals_arr):
        loc = i + 1
        formatted_val = format_to_variable_number_of_decimal_places(val, no_decimal_places)
        perc = percentage_arr[i]
        str_arr.append(f"{loc} {formatted_val} - {perc}%\n")

    return str_arr

