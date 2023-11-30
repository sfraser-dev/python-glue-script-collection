def fixed_risk_dynamic_position_size(str_arr_ents, stop_loss, full_position_size_entry1, full_position_size_avg_ent,
                                     wanted_to_risk_amount, dynamic_entry_value, is_trade_a_long):
    # dereference the passed array
    str_arr_ents = str_arr_ents[:]
    num_entries_to_process = len(str_arr_ents)
    percentage_bought_so_far_previous_ent1 = 0
    risked_amount_so_far_ent1 = 0
    data_ent1 = []
    data_avg_ent = []

    # Check that the new dynamic entry value occurs only while the trade is currently in profit
    first_entry_price, avg_entry_price, percentage_of_pos_size_bought_so_far, _ = \
        calc_average_entry_price_for_variable_entries_hit(str_arr_ents, 1)

    if (is_trade_a_long == 1) and (dynamic_entry_value <= first_entry_price):
        raise ValueError("Fixed risk dynamic position size error for long trade!")
    if (is_trade_a_long != 1) and (dynamic_entry_value >= first_entry_price):
        raise ValueError("Fixed risk dynamic position size error for short trade!")

    for i in range(1, num_entries_to_process + 1):
        first_entry_price, avg_entry_price, percentage_of_pos_size_bought_so_far, the_current_entry_price = \
            calc_average_entry_price_for_variable_entries_hit(str_arr_ents, i)

        # Calculate current risk percentage based on hit entries and stop-loss
        risk_percentage_based_on_entry1 = abs(first_entry_price - stop_loss) / first_entry_price
        risk_percentage_based_on_avg_entry = abs(avg_entry_price - stop_loss) / avg_entry_price

        # Calculate new risk percentage based on adding to the position at the current price (not moving stop-loss)
        risk_percentage_new_frdps = abs(dynamic_entry_value - stop_loss) / dynamic_entry_value

        # Entry1-only: calculate the new position size required for fixed risk dynamic position sizing
        # Entry1-only: need the percentage of total position size bought here
        percentage_bought_here_ent1 = percentage_of_pos_size_bought_so_far - percentage_bought_so_far_previous_ent1
        percentage_bought_so_far_previous_ent1 += percentage_bought_here_ent1

        # Entry1-only: calculate cumulative amount risked so far
        position_size_here_ent1 = full_position_size_entry1 * percentage_bought_here_ent1
        percentage_risked_here_ent1 = abs(the_current_entry_price - stop_loss) / the_current_entry_price
        risked_amount_here_ent1 = position_size_here_ent1 * percentage_risked_here_ent1
        risked_amount_so_far_ent1 += risked_amount_here_ent1

        # Can now finally calculate the new position size required for fixed risk dynamic position sizing
        new_amount_to_risk_ent1 = wanted_to_risk_amount - risked_amount_so_far_ent1
        new_position_size_ent1 = new_amount_to_risk_ent1 / risk_percentage_new_frdps

        # Entry1-only: output the data
        current_total_risk_ent1 = risked_amount_so_far_ent1 + new_amount_to_risk_ent1
        entry1_output = (
            f"{i}entriesHit: totRiskNow=${risked_amount_so_far_ent1:.2f}, newPosSize ${new_position_size_ent1:.0f} "
            f"at price ${the_current_entry_price:.4f} adds ${new_amount_to_risk_ent1:.2f} of risk "
            f"(totRisk now ${current_total_risk_ent1:.0f}, SL=${stop_loss:.4f})\n"
        )
        data_ent1.append(entry1_output)

        # Average-entry: calculate the new position size required for fixed risk dynamic position sizing
        risked_amount_so_far_avg_ent = full_position_size_avg_ent * percentage_of_pos_size_bought_so_far * \
                                       risk_percentage_based_on_avg_entry
        new_amount_to_risk_avg_ent = wanted_to_risk_amount - risked_amount_so_far_avg_ent
        new_position_size_avg_ent = new_amount_to_risk_avg_ent / risk_percentage_new_frdps

        # Average-entry: output the data
        current_total_risk_avg_ent = risked_amount_so_far_avg_ent + new_amount_to_risk_avg_ent
        avg_entry_output = (
            f"{i}entriesHit: totRiskNow=${risked_amount_so_far_avg_ent:.2f}, newPosSize ${new_position_size_avg_ent:.0f} "
            f"at price ${the_current_entry_price:.4f} adds ${new_amount_to_risk_avg_ent:.2f} of risk "
            f"(totRisk now ${current_total_risk_avg_ent:.0f}, SL=${stop_loss:.4f})\n"
        )
        data_avg_ent.append(avg_entry_output)

    return data_ent1, data_avg_ent


def calc_average_entry_price_for_variable_entries_hit(str_arr_ents, entries_hit):
    str_arr_ents = str_arr_ents[:entries_hit]
    first_entry_price = float(str_arr_ents[0].split()[3])
    avg_entry_price = sum(float(line.split()[3]) for line in str_arr_ents) / entries_hit
    percentage_of_pos_size_bought_so_far = float(str_arr_ents[-1].split()[3].rstrip('%'))
    current_entry_price = float(str_arr_ents[-1].split()[3])
    return first_entry_price, avg_entry_price, percentage_of_pos_size_bought_so_far, current_entry_price
