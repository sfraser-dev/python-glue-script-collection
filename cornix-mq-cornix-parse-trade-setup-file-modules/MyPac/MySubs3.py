def calc_average_entry_price_for_variable_entries_hit(str_arr_ents, num_of_entries_to_use_for_calculation):
    arbitrary_position_value = 100000
    total_number_coins_bought = 0
    total_amount_paid_for_coins = 0
    first_entry_price = None
    total_percentage_of_position_size_bought = 0

    for i in range(num_of_entries_to_use_for_calculation):
        splitter = str_arr_ents[i].split()
        entry_price = float(splitter[1])
        
        if i == 0:
            first_entry_price = entry_price
        
        percentage = float(splitter[3].replace('%', '')) / 100
        total_percentage_of_position_size_bought += percentage

        amount_spent_at_this_entry_point = arbitrary_position_value * percentage
        number_coins_bought_at_this_entry_point = amount_spent_at_this_entry_point / entry_price
        
        total_amount_paid_for_coins += amount_spent_at_this_entry_point
        total_number_coins_bought += number_coins_bought_at_this_entry_point

        entry_price_final_i = entry_price

    average_entry_price = total_amount_paid_for_coins / total_number_coins_bought

    return first_entry_price, average_entry_price, total_percentage_of_position_size_bought, entry_price_final_i


def risk_softening_multiplier(str_arr_ents, stop_loss):
    num_entries_hit = len(str_arr_ents)
    first_entry_price, avg_entry_price, percentage_of_pos_size_bought_so_far, dummy_var = \
        calc_average_entry_price_for_variable_entries_hit(str_arr_ents, num_entries_hit)

    risk_percentage_based_on_entry1 = abs(first_entry_price - stop_loss) / first_entry_price
    risk_percentage_based_on_avg_entry = abs(avg_entry_price - stop_loss) / avg_entry_price
    risk_soft_mult = risk_percentage_based_on_avg_entry / risk_percentage_based_on_entry1

    return risk_soft_mult, risk_percentage_based_on_entry1, risk_percentage_based_on_avg_entry
