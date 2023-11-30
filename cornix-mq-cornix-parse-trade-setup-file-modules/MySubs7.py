def format_to_variable_number_of_decimal_places(val_in, decimal_places):
    # sprintf("%.Xf",str) where X is variable
    template = f"%.{decimal_places}f"
    val_out = template % val_in
    return val_out

