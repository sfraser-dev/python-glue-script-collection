def calc_average_entry_price_for_variable_entries_hit(entries_arr, num_entries_to_use):
    arbitrary_position_value = 100000
    total_number_coins_bought = 0
    total_amount_paid_for_coins = 0
    first_entry_price = None
    total_percentage_of_position_size_bought = 0

    for i in range(num_entries_to_use):
        # Extract values and percentages from the Cornix Entry Targets string array
        entry_details = entries_arr[i].split(" ")
        entry_price = float(entry_details[1])
        if i == 0:
            first_entry_price = entry_price

        percentage = float(entry_details[3].strip("%")) / 100
        total_percentage_of_position_size_bought += percentage

        # Calculate number of coins bought at this entry and percentage (using the same arbitrary position size as the spreadsheet)
        amount_spent_at_this_entry_point = arbitrary_position_value * percentage
        number_coins_bought_at_this_entry_point = amount_spent_at_this_entry_point / entry_price

        total_amount_paid_for_coins += amount_spent_at_this_entry_point
        total_number_coins_bought += number_coins_bought_at_this_entry_point

        entry_price_final = entry_price

    average_entry_price = total_amount_paid_for_coins / total_number_coins_bought

    return (
        first_entry_price,
        average_entry_price,
        total_percentage_of_position_size_bought,
        entry_price_final
    )

