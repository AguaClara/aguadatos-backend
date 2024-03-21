#generalized mismatch error message
def mismatch_error(key, expected, got):
        """
        Constructs a standardized error message for assertion mismatches.

        :param key: The key or attribute name being tested.
        :param expected: The expected value.
        :param got: The actual value obtained.
        :return: A formatted error message string.
        """
        return f"Mismatch in {key}: Expected '{expected}' for '{key}', but got '{got}' instead."
