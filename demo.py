from collatz_machine import CollatzMachine

def bits_lsb(n):
    return list(map(int, bin(n)[2:][::-1]))

def run_collatz_chain(start_value, max_steps=1000, debug=False):
    results = []
    
    current_input = start_value
    steps = 0

    while current_input != 1 and steps < max_steps:
        m = CollatzMachine(debug=debug)
        bits = bits_lsb(current_input)

        for b in bits:
            m.nextbit(b)
        m.end_of_input()

        report = m.report()
        results.append((current_input, report['output_decimal']))
        current_input = report['output_decimal']
        steps += 1

    if current_input == 1:
        results.append((1, 1))

    return results

if __name__ == "__main__":
    chain = run_collatz_chain(27, debug=True)

    print("\n--- Collatz Chain for 27 ---")
    for i, (n, next_n) in enumerate(chain):
        print(f"Step {i}: {n} → {next_n}")

