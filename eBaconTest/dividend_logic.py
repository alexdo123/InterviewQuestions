import json

def parse_amount(value):
    """Convert '$100' -> 100.0 or just pass through numbers."""
    if isinstance(value, str) and value.startswith("$"):
        return float(value.replace("$", "").replace(",", ""))
    return float(value)

def distribute_dividends(dividend_data, employee_data):
    results = []

    for div in dividend_data['DividendAmounts']:
        inv = div['Investment']
        total_dividend = parse_amount(div['Amount'])

        # Convert employee amounts
        total_holding = sum(parse_amount(e['Amount']) for e in employee_data['EmployeeData'] if e['Investment'] == inv)

        for e in employee_data['EmployeeData']:
            if e['Investment'] == inv:
                share = parse_amount(e['Amount']) / total_holding
                payout = total_dividend * share
                results.append({
                    "Name": e['Name'],
                    "Investment": inv,
                    "Payout": f"${payout:.2f}"
                })

    # Sort results so the same person’s records appear together
    results.sort(key=lambda x: x["Name"])
    return results


if __name__ == "__main__":
    with open("DividendLogicTest.json") as f:
        data = json.load(f)

    output = distribute_dividends(data, data)
    print(json.dumps(output, indent=2))
