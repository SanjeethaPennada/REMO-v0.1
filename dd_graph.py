import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

PASS = 0
FAIL = 1


def induce_failure(x, F):
    """ Simulate a test failure induced by the input x and the set of failure-inducing entities F.
    Return PASS if the failure is not induced, FAIL otherwise. """
    for subset in F:
        if set(subset).issubset(set(x)):
            return FAIL
    return PASS

def ddmin(test, inp, F):
    """Reduce the input inp, using the outcome of test(fun, inp)."""
    assert test(inp) != PASS

    n = 2     # Initial granularity
    num_steps = 0
    while len(inp) >= 2:
        start = 0
        subset_length = len(inp) // n
        some_complement_is_failing = False

        while start < len(inp):
            complement = inp[:start] + inp[start + subset_length:]
            error_triggered = test(complement) == FAIL
            num_steps += 1
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
     
    return inp, num_steps

def run_dd(start_n, end_n, F):
    # Delta Debugging implementation code 
    # Returns the reduced input sequence and the number of steps
    input_sequence = list(range(1, end_n + 1))
    reduced_sequence, num_steps = ddmin(lambda x: induce_failure(x, F), input_sequence, F)
    return reduced_sequence, num_steps

def generate_output():
    try:
        # Get selected start and end n values which is input size
        start_n = int(start_n_entry.get())
        end_n = int(end_n_entry.get())

        # Get F set from the entry widget
        F_set = eval(F_entry.get())  # Assuming F is entered as a list of lists
        
        # Validate F to ensure it's a list of lists
        if not isinstance(F_set, list) or not all(isinstance(subset, list) for subset in F_set):
            messagebox.showerror("Invalid Input", "F must be a list of lists. E.g., [[1, 2], [3, 4]]")
            return

        # Run Delta Debugging and get the output
        output_sequence, num_steps = run_dd(start_n, end_n, F_set)

        # Display the output
        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Reduced Input Sequence:\n")
        output_text.insert(tk.END, str(output_sequence))
        output_text.insert(tk.END, "\n\nNumber of Steps: ")
        output_text.insert(tk.END, str(num_steps))
        output_text.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.title("Delta Debugging GUI")

# Label and entry for entering start and end n values
start_n_label = tk.Label(root, text="Start from:")
start_n_label.grid(row=0, column=0)
start_n_entry = tk.Entry(root)
start_n_entry.grid(row=0, column=1)

end_n_label = tk.Label(root, text="End at:")
end_n_label.grid(row=1, column=0)
end_n_entry = tk.Entry(root)
end_n_entry.grid(row=1, column=1)

# Label and entry for entering F set
F_label = tk.Label(root, text="Enter F set (list of lists):")
F_label.grid(row=2, column=0)
F_entry = tk.Entry(root)
F_entry.grid(row=2, column=1)

# Button to generate the output
generate_button = tk.Button(root, text="Run Delta Debugging", command=generate_output)
generate_button.grid(row=3, column=0, columnspan=2)

# Text widget to display the output
output_text = tk.Text(root, height=10, width=40)
output_text.grid(row=4, column=0, columnspan=2)
output_text.config(state=tk.DISABLED)

root.mainloop()

