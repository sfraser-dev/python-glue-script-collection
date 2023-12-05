def format_to_variable_number_of_decimal_places(val_in: float, decimal_places: int) -> str:
    temp = f"%.{decimal_places}f"
    val_out = temp % val_in
    return val_out