# -*- coding: utf-8 -*-
"""
Created on Mon May 13 21:41:45 2024

@author: Sanjeetha Pennada
"""

#Delta Debugging implements the strategy sketched above: It first removes larger chunks
# of size  12 ; if this does not fail, then we proceed to chunks of size  14  , 
#then  18 and so on. Our ddmin() implementation uses the exact same Python 
#code as Zeller in [Zeller et al, 2002]; the only difference is that it has been 
#adapted to work on Python 3. The variable n (initially 2) indicates the granularity – 
#in each step, chunks of size  1n are cut away. If none of the test fails
# (some_complement_is_failing is False), then n is doubled – until it reaches the 
#length of the input.
  
from typing import Callable, Sequence, Any

PASS = 0
FAIL = 1

def induce_failure(x: Sequence, F: Sequence[Sequence[int]]) -> int:
    """ Simulate a test failure induced by the input x and the set of failure-inducing entities F.
    Return PASS if the failure is not induced, FAIL otherwise. """
    for subset in F:
        if set(subset).issubset(set(x)):
            return FAIL
    return PASS

def ddmin(test: Callable, inp: Sequence, *test_args: Any) -> Sequence:
    """Reduce the input inp, using the outcome of test(fun, inp)."""
    assert test(inp, *test_args) != PASS
    

    n = 2     # Initial granularity
    print("Step | Subsequence            | Error Triggered")
    print("---------------------------------------------")
    while len(inp) >= 2:
        start = 0
        subset_length = int(len(inp) / n)
        some_complement_is_failing = False

        while start < len(inp): #The input (inp) is updated to the current subset (complement) that triggered the failure. i/p reduced to subset that caused the failure.
            complement = (inp[:int(start)] + inp[int(start + subset_length):])
            error_triggered = test(complement, *test_args) == FAIL
            print(f"{n:<5} | {complement}{' '*(25-len(str(complement)))}| {'✓' if error_triggered else '❌'}")
            if error_triggered:
                inp = complement
                n = max(n - 1, 2)
                some_complement_is_failing = True
                break

            start += subset_length

        if not some_complement_is_failing:
            if n == len(inp):
                break
            n = min(n * 2, len(inp))
     
    return inp

# Example usage
if __name__ == "__main__":
    # Original test input and failure-inducing sets
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    F = [[1, 8]]

    # Define test function
    def test_function(inp):
        return induce_failure(inp, F)

    # Apply Delta Debugging algorithm
    minimal_input = ddmin(test_function, x)
    print("Minimal Failure-inducing input found input found:", minimal_input)