class CollatzMachine:
    _instance_counter = 0

    def __init__(self, downstream=None, debug=False):
        self.id = CollatzMachine._instance_counter
        CollatzMachine._instance_counter += 1

        self.input_bits = []        # LSB-first input bits
        self.output_bits = []       # LSB-first output bits (n // 2 or 3n+1)
        self.input_done = False
        self.finalized = False
        self.downstream = downstream
        self.debug = debug

        if self.debug:
            print(f"[Machine {self.id}] Initialized")

    def nextbit(self, bit):
        if self.input_done:
            raise RuntimeError("Cannot add bits after end_of_input")
        if bit not in (0, 1):
            raise ValueError("Bit must be 0 or 1")
        self.input_bits.append(str(bit))
        if self.debug:
            print(f"[Machine {self.id}] Received input bit: {bit}")

    def end_of_input(self):
        if self.input_done:
            return
        self.input_done = True

        n = int(''.join(self.input_bits[::-1]), 2)  # Reconstruct original number
        if self.debug:
            print(f"[Machine {self.id}] Input decimal: {n}")

        if n == 0:
            result = 0
        elif n % 2 == 0:
            result = n // 2
            if self.debug:
                print(f"[Machine {self.id}] Even → {n} // 2 = {result}")
        else:
            result = 3 * n + 1
            if self.debug:
                print(f"[Machine {self.id}] Odd → 3*{n} + 1 = {result}")

        # Convert result to LSB-first binary
        if result == 0:
            self.output_bits = ['0']
        else:
            self.output_bits = list(bin(result)[2:])[::-1]

        if self.debug:
            print(f"[Machine {self.id}] Output bits (LSB first): {self.output_bits}")

        # Emit to downstream
        if self.downstream:
            for b in self.output_bits:
                self.downstream.nextbit(int(b))
            self.downstream.end_of_input()

        self.finalized = True

    def report(self):
        input_dec = int(''.join(self.input_bits[::-1]), 2) if self.input_bits else 0
        output_dec = int(''.join(self.output_bits[::-1]), 2) if self.output_bits else 0
        return {
            'id': self.id,
            'input_bits': self.input_bits,
            'input_decimal': input_dec,
            'output_bits': self.output_bits,
            'output_decimal': output_dec,
            'finalized': self.finalized
        }


if __name__ == "__main__":
    #m = make_recursive_machine([1, 0, 1])
    # Define a chain depth of 3
    m6 = CollatzMachine(debug=True)
    m5 = CollatzMachine(downstream=m6, debug=True)
    m4 = CollatzMachine(downstream=m5, debug=True)
    m3 = CollatzMachine(downstream=m4, debug=True)
    m2 = CollatzMachine(downstream=m3, debug=True)
    m1 = CollatzMachine(downstream=m2, debug=True)
    
    # Input 5 (binary: 101, LSB-first)
    for b in [1, 0, 1]:
        m1.nextbit(b)
    
    m1.end_of_input()
    print(m1.report())
    print(m2.report())
    print(m3.report())
    print(m4.report())
    print(m5.report())
    print(m6.report())

