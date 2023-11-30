import datetime

def create_output_filename(script_name, pair, is_trade_a_long):
    # Remove '.pl' from script name
    script_name = script_name[:-3]

    # Get current date and time
    current_time = datetime.datetime.now()

    # Format date and time
    date_str = current_time.strftime("%Y%m%d---%H%M_%S")
    pair_no_slash = pair.replace('/', '')

    # Determine long or short string
    if is_trade_a_long:
        long_or_short_str = "long"
    else:
        long_or_short_str = "short"

    # Construct output file name
    output_file_name = f"{date_str}---{pair_no_slash}-{long_or_short_str}.trade"

    return output_file_name

