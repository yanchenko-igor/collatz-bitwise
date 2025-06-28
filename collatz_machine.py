class CollatzStep:
    def __init__(self, input_value, step_index):
        self.input_value = input_value
        self.result_value = None
        self.step_index = step_index
        self.finalized = False  # Marks if input is closed for this step
        self.next_step = None

    def compute_result(self):
        if self.input_value % 2 == 0:
            self.result_value = self.input_value // 2
        else:
            self.result_value = 3 * self.input_value + 1
        return self.result_value

    def update_input(self, new_input):
        if self.input_value != new_input:
            self.input_value = new_input
            self.compute_result()
            return True  # changed
        return False  # no change


class CollatzHistory:
    def __init__(self):
        self.steps = []
        self.input_closed = False

    def _create_first_step(self, initial_input):
        step = CollatzStep(initial_input, 0)
        step.compute_result()
        self.steps = [step]

    def add_or_update_input(self, new_input):
        if not self.steps:
            self._create_first_step(new_input)
        else:
            changed = self.steps[0].update_input(new_input)
            if changed:
                self._recalculate_downstream(start_index=0)

        # After updating input, if input NOT closed, we run as far as possible
        if not self.input_closed:
            self._extend_steps_open_input()

    def _recalculate_downstream(self, start_index):
        for i in range(start_index, len(self.steps) - 1):
            current_step = self.steps[i]
            next_step = self.steps[i + 1]
            updated = next_step.update_input(current_step.result_value)
            if not updated:
                break

    def _extend_steps_open_input(self):
        # For open input, we only extend the history if result_value == 1
        # or if current steps can continue with known info
        while len(self.steps) > 0:
            last_step = self.steps[-1]
            if last_step.result_value == 1:
                break
            # Do NOT add new steps when input is open (unknown future input)
            # But can continue if next step exists
            next_index = last_step.step_index + 1
            if next_index < len(self.steps):
                last_step = self.steps[next_index]
            else:
                # Can't extend because input is open and no next step info
                break

    def finalize_input(self):
        self.input_closed = True
        # On input closed, extend sequence until 1
        while True:
            last_step = self.steps[-1]
            if last_step.result_value == 1:
                break
            new_step = CollatzStep(last_step.result_value, len(self.steps))
            new_step.compute_result()
            self.steps.append(new_step)

    def print_progress(self):
        print(f"\nCurrent number: {self.steps[0].input_value}")
        print(f"Steps counted so far: {len(self.steps) - 1}")
        for step in self.steps:
            iv = step.input_value
            rv = step.result_value
            si = step.step_index
            if iv % 2 == 0:
                print(f"Step {si}: Even → {rv}")
            else:
                print(f"Step {si}: Odd → 3n+1 = {rv}")

    def print_final_summary(self):
        print(f"\n✅ Sequence ended in {len(self.steps) - 1} steps.")
        print(f"Initial number: {self.steps[0].input_value}")
        highest = max(step.input_value for step in self.steps)
        print(f"Highest number reached: {highest}")

class CollatzMachine:
    def __init__(self):
        self.decimal_input = ''
        self.history = CollatzHistory()

    def feed_decimal_digits(self, digits):
        self.decimal_input = digits + self.decimal_input
        new_initial = int(self.decimal_input)
        print(f"Collected decimal input: {self.decimal_input}")
        self.history.add_or_update_input(new_initial)
        self.history.print_progress()

    def end_input(self):
        print("\nInput closed by user.")
        self.history.finalize_input()
        self.history.print_final_summary()
        self.reset()

    def reset(self):
        self.decimal_input = ''
        self.history = CollatzHistory()


def main():
    machine = CollatzMachine()
    print("Enter digits in normal order (e.g., 1501).")
    print("Type digits one by one, building the number from MSB.")
    print("Press ENTER on an empty line to finalize input and run to completion.")
    print("Type 'exit' to quit.\n")

    while True:
        line = input(">> ").strip()
        if line.lower() == 'exit':
            break
        elif line == '':
            if machine.decimal_input == '':
                print("No input collected yet.")
            else:
                machine.end_input()
        elif line.isdigit():
            machine.feed_decimal_digits(line)
        else:
            print("⚠ Invalid input. Enter digits or empty line to finish.")

if __name__ == "__main__":
    main()

