def safeInput(prompt):
    """Get a non-negative integer input with error handling."""
    while True:
        try:
            value=int(input(prompt))
            if value<0:
                raise ValueError("Value must be non-negative")
            return value
        except ValueError as error:
            print(f"Invalid input: {error}. Please try again.")
