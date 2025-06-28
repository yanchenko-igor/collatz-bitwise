from collections import deque

class CollatzMachine:
    def __init__(self):
        self.decimal_input = ''
        self.collatz_n = None
        self.step = 0
        self.started = False
        self.end_of_input = False
        self.waiting_for_input = False
        self.processed_steps = []  # Track already processed numbers to avoid recounting
        self.full_history = []  # Store full Collatz values for recomputation

    def feed_decimal_digits(self, digits):
        self.decimal_input = digits + self.decimal_input  # Prepend new digits as MSB
        print(f"Collected decimal input: {self.decimal_input}")
        new_input_value = int(self.decimal_input)

        # Recalculate from the beginning
        self.collatz_n = new_input_value
        if not self.started:
            print(f"\n▶ Starting Collatz on {self.collatz_n} (from full decimal input)")
            self.started = True
        else:
            print(f"\n▶ New input merged. Recalculating Collatz sequence for {self.collatz_n}.")

        self.step = 0
        self.full_history = []
        self.processed_steps = []
        self.waiting_for_input = False
        self.run_until_wait_or_done()

    def run_until_wait_or_done(self):
        while True:
            if self.collatz_n == 1:
                if self.end_of_input:
                    print(f"✅ Sequence ended in {self.step} steps.")
                    self.reset()
                else:
                    print("Sequence reached 1, but input is still open, waiting for more digits...")
                    self.waiting_for_input = True
                break

            if self.waiting_for_input:
                break

            if self.collatz_n in self.processed_steps:
                break
            else:
                self.processed_steps.append(self.collatz_n)
                self.full_history.append(self.collatz_n)

            if self.collatz_n % 2 == 0:
                self.collatz_n //= 2
                print(f"Step {self.step}: Even → {self.collatz_n}")
            else:
                self.collatz_n = 3 * self.collatz_n + 1
                print(f"Step {self.step}: Odd → 3n+1 = {self.collatz_n}")

            self.step += 1

        if self.end_of_input and self.collatz_n == 1:
            print(f"✅ Final summary: Total steps = {self.step}.")
            self.reset()

    def end_input(self):
        self.end_of_input = True
        self.waiting_for_input = False
        if self.started:
            self.run_until_wait_or_done()

    def reset(self):
        print("Sequence complete, resetting input.\n")
        self.decimal_input = ''
        self.collatz_n = None
        self.started = False
        self.waiting_for_input = False
        self.end_of_input = False
        self.step = 0
        self.processed_steps = []
        self.full_history = []

def main():
    machine = CollatzMachine()
    print("Enter digits in normal order (e.g., 1501).")
    print("Press ENTER on an empty line to continue or end input.")
    print("Type 'exit' to quit.\n")

    while True:
        line = input(">> ").strip()
        if line.lower() == 'exit':
            break
        elif line == '':
            machine.end_input()
        elif line.isdigit():
            machine.feed_decimal_digits(line)
        else:
            print("⚠ Invalid input. Please enter digits or press ENTER.")

if __name__ == "__main__":
    main()

