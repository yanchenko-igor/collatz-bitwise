class VirtualMemoryCollatzMachine:
    def __init__(self, n, debug=False):
        self.debug = debug
        self.step_count = 0

        # True internal value, not truncated
        self.true_value = n

        # Initial tape: bits in LSB-first order (index 0 is LSB)
        bin_n = bin(n)[2:]
        self.tape = list(bin_n.zfill(len(bin_n) + 1))[::-1]  # extra zero for MSB padding
        self.tape_len = len(self.tape)

        # Overflow tape: holds extra MSBs beyond tape capacity
        self.overflow_tape = []

    def current_state(self):
        return ''.join(self.tape[::-1])  # show MSB-first for human view

    def value_from_tape(self):
        return int(''.join(self.tape[::-1]), 2)

    def step(self):
        self.step_count += 1

        if self.debug:
            print(f"\nStep {self.step_count}")
            print(f"Before: bits={self.current_state()}  value={self.true_value}")

        # --- Compute 3n + 1 or n // 2 using true value ---
        if self.true_value % 2 == 0:
            self.true_value //= 2
        else:
            self.true_value = 3 * self.true_value + 1

        new_bin = bin(self.true_value)[2:]  # strip '0b'
        new_bits = list(new_bin)

        # --- Handle overflow ---
        overflow_len = max(0, len(new_bits) - self.tape_len)
        if overflow_len > 0:
            self.overflow_tape = new_bits[:overflow_len]
            new_bits = new_bits[overflow_len:]
        else:
            self.overflow_tape = []

        # --- Write to tape (LSB-first) ---
        self.tape = new_bits[::-1]  # reverse for LSB-first

        # If tape shrank, pad with zeros to maintain tape_len
        self.tape += ['0'] * (self.tape_len - len(self.tape))

        if self.debug:
            print(f"After:  bits={self.current_state()}  value={self.true_value}")
            if self.overflow_tape:
                print(f"Overflow tape: {''.join(self.overflow_tape)}")

        return self.true_value != 1

    def run(self):
        print(f"Start: bits={self.current_state()}  value={self.true_value}")
        while self.step():
            pass
        print(f"\n✅ Collapsed in {self.step_count} steps.")


if __name__ == "__main__":
    machine = VirtualMemoryCollatzMachine(27, debug=True)
    machine.run()

