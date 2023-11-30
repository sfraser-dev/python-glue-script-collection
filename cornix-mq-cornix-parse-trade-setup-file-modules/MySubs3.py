def risk_softening_multiplier(entries_arr, stop_loss):
    # Assume advanced template entries are in the correct order (long or short)

    num_entries_hit = len(entries_arr)

    first_entry_price, avg_entry_price, percentage_of_pos_size_bought_so_far, _ = calc_average_entry_price_for_variable_entries_hit(entries_arr, num_entries_hit)

    # Calculate risk percentage based on the first entry (entry1) and average entry, and a risk-softening-multiplier (the risk-softening-multiplier is just for entry1 calculation)

    risk_percentage_based_on_entry1 = abs(first_entry_price - stop_loss) / first_entry_price
    risk_percentage_based_on_avg_entry = abs(avg_entry_price - stop_loss) / avg_entry_price
    risk_soft_mult = risk_percentage_based_on_avg_entry / risk_percentage_based_on_entry1

    return (risk_soft_mult, risk_percentage_based_on_entry1, risk_percentage_based_on_avg_entry)

