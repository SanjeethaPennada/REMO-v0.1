def ddmin(elements, test_func):
    """
    Delta Debugging algorithm to find the smallest subsequence of elements that still triggers the error.
    """
    n = len(elements) // 2  # Initial length of subsequence
    step = 1
    while n >= 1:
        print("| Step | Subsequence                | Error Triggered |")
        print("|------|----------------------------|-----------------|")
        # Test consecutive subsequences of length n
        for i in range(len(elements) - n + 1):
            subsequence = elements[i:i+n]
            error_triggered = test_func(subsequence)
            print(f"| {step:<5}| {''.join(subsequence):<27}| {'T' if error_triggered else 'F':<15}|")
            step += 1
            if error_triggered:
                return subsequence
        
        # Test complements of consecutive subsequences of length n
        for i in range(len(elements) - n + 1):
            subsequence = elements[:i] + elements[i+n:]
            error_triggered = test_func(subsequence)
            print(f"| {step:<5}| {''.join(subsequence):<27}| {'T' if error_triggered else 'F':<15}|")
            step += 1
            if error_triggered:
                return subsequence
        
        n = max(1, n // 2)  # Reduce the length of subsequence by half

    # If no subsequence triggers the error, return the original elements
    return elements

def buggy_function(subsequence):
    """
    Function to test if a subsequence triggers the error.
    """
    try:
        # Execute the provided program with the subsequence
        exec(''.join(subsequence))
        # Assume the error is triggered if the execution completes without error
        return False
    except Exception as e:
        # If an error occurs during execution, consider it as buggy
        return True

# Define the program as a list of statements
program = [
    "import tensorflow as tf\n",
    "x = tf.constant(3.0)\n",
    "b = 1.0\n",
    "with tf.GradientTape() as tape:\n",
    "    tape.watch(x)\n",
    "    y = x ** 2\n",
    "    b = tape.gradient(y, x)\n",
    "print(type(b))\n"
]

# Apply ddmin to find the minimal subsequence that triggers the error
minimal_subsequence = ddmin(program, buggy_function)

# Print the minimal subsequence
print("Minimal subsequence:")
print(''.join(minimal_subsequence))
