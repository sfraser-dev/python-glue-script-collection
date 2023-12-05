def calc_average_entry_price_for_variable_entries_hit(str_arr_ents, num_of_entries_to_use_for_calculation):
    # Dereference the passed array
    str_arr_ents = str_arr_ents.tolist()

    # Assigns arbitary position value for ease of claculation. Based on this arbitary position value, calc number of coins
    # bought at each entry point (using entry price & assigned percentage of position size). Keep a running total of amount of
    # coins bought and a running total paid for these coins (total paid will be the full arbitary value *IF* all entry targets hit).
    # If not all entry targets hit, it will be a different total amount paid.
    # Note: the amount used for the arbitary position value doesn't matter, it'll give the same result
    arbitrary_position_value = 100000
    total_number_coins_bought = 0
    total_amount_paid_for_coins = 0
    first_entry_price = None
    total_percentage_of_position_size_bought = 0

    for i in range(num_of_entries_to_use_for_calculation):
        # get the values and percentages from the Cornix Entry Tragets: string array
        splitter = str_arr_ents[i].split()  # split line using spaces, [0]=1), [1]=value, [2]=hyphen, [3]=percentage
        entry_price = float(splitter[1])

        if i == 0:
            first_entry_price = entry_price

        percentage = float(splitter[3].replace("%", "")) / 100  # percentage as decimal
        total_percentage_of_position_size_bought += percentage

        # calculate "number of coins obtained" at this entry and percentage (using arbitary position size same as spreadsheet)
        amount_spent_at_this_entry_point = arbitrary_position_value * percentage
        number_coins_bought_at_this_entry_point = amount_spent_at_this_entry_point / entry_price

        total_amount_paid_for_coins += amount_spent_at_this_entry_point
        total_number_coins_bought += number_coins_bought_at_this_entry_point

    average_entry_price = total_amount_paid_for_coins / total_number_coins_bought

    return first_entry_price, average_entry_price, total_percentage_of_position_size_bought


def risk_softening_multiplier(str_arr_ents, stop_loss):
    # Dereference the passed array
    str_arr_ents = str_arr_ents.tolist()

    num_entries_hit = len(str_arr_ents)
    first_entry_price, avg_entry_price, percentage_of_pos_size_bought_so_far, _ = calc_average_entry_price_for_variable_entries_hit(str_arr_ents, num_entries_hit)

    # calculate risk percentatge based on just the first entry (entry1), risk percentage based on average entry and a
    # risk-softening-multiplier (the risk-softening-multiplier is just for entry1 calculation)
    #
    # What is risk-softening-multiplier? I would use TradingView's RR tool to get the SL distance from the FIRST entry;
    # I would then use this risk percentage to calculate my total position size. When I started layering multiple bids below
    # the FirstEntry, I kept using ONLY the first entry to calcualte my risk - my risk WASN'T this much as I would have an average
    # bid entry below this due to layering my bids. The risk-softening-multiplier accounts for this. If I wanted to risk $100 on 
    # a trade and used only the first entry to calculate this risk (but actually had layered bids), my risk-softening-multiplier
    # might be something like 0.75, thus my actual risk would only be $100*0.75 = $75. I never used to layer bids so this was a simple
    # way for me implement it initially - easy for me to update my journal properly and quickly if I calcualed my risk using only
    # the first entry but actually had layered bids.

    risk_percentage_based_on_entry1 = abs(first_entry_price - stop_loss) / first_entry_price

