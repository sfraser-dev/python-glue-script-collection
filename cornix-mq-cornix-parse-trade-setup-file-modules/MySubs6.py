import ListUtil

def heavy_weighting_at_entry_or_stoploss(entries_or_targets_str, no_of_entries, high, low, is_trade_a_long, weighting_factor,
                                           no_decimal_places):
    str_arr = MySubs2.even_distribution(entries_or_targets_str, no_of_entries, high, low, is_trade_a_long, no_decimal_places)

    percentages = []
    for line in str_arr:
        splitter = line.split(" ")
        percentage = float(splitter[3].strip("%"))
        percentages.append(percentage)

    arr_length_perc = len(percentages)
    mod = arr_length_perc % 2
    is_even = True if mod == 0 else False

    temp = []
    for i in range(int(arr_length_perc / 2)):
        temp.append(i)
        temp.append(arr_length_perc - 1 - i)

    index_pairs = ListUtil.pairs(temp)

    for x in range(int(arr_length_perc / 2)):
        for i in range(int(arr_length_perc / 2) - x):
            percentages[i] -= weighting_factor
            percentages[index_pairs[i][1]] += weighting_factor

    str_arr_new_percentages = []
    for line in str_arr:
        splitter = line.split(" ")
        num = splitter[0]
        val = splitter[1]
        hash = splitter[2]
        per = format(percentages[int(num)], ".2f")
        if float(per) <= 0:
            raise Exception("error: percentage weighting is zero or less")

        newline = f"{num} {val} {hash} {per}%\n"
        str_arr_new_percentages.append(newline)

    return str_arr_new_percentages

