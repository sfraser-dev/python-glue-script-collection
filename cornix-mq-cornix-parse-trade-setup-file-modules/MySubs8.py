def calc_risk_added_at_each_entry(entries_arr, num_entries, stop_loss, full_position_size, wanted_to_risk_amount):
    total_risk_so_far = 0
    ret_arr = []

    for i in range(num_entries):
        # Extract values and percentages from the Cornix Entry Tragets string array
        entry_details = entries_arr[i].split(" ")
        entry_price = float(entry_details[1])
        percentage = float(entry_details[3].strip("%")) / 100

        entry_no = i + 1
        this_entry_position_size = full_position_size * percentage
        this_risked_percentage = abs(entry_price - stop_loss) / entry_price
        this_risked_amount = this_entry_position_size * this_risked_percentage

        total_risk_so_far += this_risked_amount
        amount_still_left_to_risk = wanted_to_risk_amount - total_risk_so_far

        str1 = f"entry {entry_no}: riskAmountAddedHere=$%.2f, totRiskNow=$%.2f ($%.2f-$%.2f=$%.2f still to risk)" % (
            this_risked_amount, total_risk_so_far, wanted_to_risk_amount, total_risk_so_far, amount_still_left_to_risk)
        ret_arr.append(str1)

    return ret_arr

