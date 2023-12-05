import MyPac.MySubs5
import MyPac.MySubs6

def create_cornix_free_text_simple_template(pair, leverage, high_entry, low_entry, high_target, low_target, stop_loss, no_decimal_places, num_entries, num_targets, is_trade_a_long):
    simple_template = []

    simple_template.append("########################### simple template")
    simple_template.append(pair)

    # If leverage is greater than or equal to 1, append the leverage line to the template
    if leverage >= 1:
        simple_template.append(f"leverage cross {leverage}x")

    # Format stop-loss to the specified number of decimal places
    formatted_stop_loss = MyPac.MySubs6.format_to_variable_number_of_decimal_places(stop_loss, no_decimal_places)

    # Set weighting factors to 0 since Cornix Free Text simple mode cannot set percentage weighting factors
    weighting_factor_entries = 0
    weighting_factor_targets = 0

    # Get entry strings with heavy weighting at entry or stop-loss
    entry_strings = MyPac.MySubs5.heavy_weighting_at_entry_or_stop_loss("entries", num_entries, high_entry, low_entry, is_trade_a_long, weighting_factor_entries, no_decimal_places)

    # Get target strings
    target_strings = MyPac.MySubs5.heavy_weighting_at_entry_or_stop_loss("targets", num_targets, high_target, low_target, is_trade_a_long, weighting_factor_targets, no_decimal_places)

    # Extract entry values from entry strings
    entry_values = []
    for entry_string in entry_strings:
        entry_value = float(entry_string.split()[1])
        entry_values.append(MyPac.MySubs6.format_to_variable_number_of_decimal_places(entry_value, no_decimal_places))

    # Extract target values from target strings
    target_values = []
    for target_string in target_strings:
        target_values.append(float(target_string.split()[1]))

    # Construct the "enter" line with entry values
    simple_template.append("enter")
    for entry_value in entry_values:
        simple_template.append(f"{entry_value} ")

    # Add the stop-loss line
    simple_template.append(f"\nstop {formatted_stop_loss}")

    # Construct the "targets" line with target values
    simple_template.append("\ntargets")
    for target_value in target_values:
        simple_template.append(f"{target_value} ")

    return simple_template

