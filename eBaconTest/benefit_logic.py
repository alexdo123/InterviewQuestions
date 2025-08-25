import json

def calculate_benefits(benefit_total_data, allocations, investments):
    benefit_results = []
    investment_results = []

    for emp in allocations['BenefitAllocations']:
        name = emp['employee']
        benefit_total = benefit_total_data[name]['benefitTotal']

        # Calculate benefits as percentages
        benefit_dict = {}
        for d in emp['BenefitPercent']:
            for k, v in d.items():
                benefit_dict[k] = f"{v}%"  # add % sign
        benefit_results.append({"employee": name, **benefit_dict})

        # Calculate investment percentages based on 401K
        if '401K' in benefit_dict:
            invest_info = next((i for i in investments['InvestmentAllocations'] if i['employee'] == name), None)
            if invest_info:
                inv_dict = {}
                k401_percent = float(benefit_dict['401K'].replace("%",""))
                for d in invest_info['InvestmentsPercent']:
                    for k, v in d.items():
                        inv_dict[k] = f"{round(k401_percent * v / 100, 2)}%"  # multiply and add %
                investment_results.append({"employee": name, **inv_dict})

    return benefit_results, investment_results


if __name__ == "__main__":
    with open("PunchLogicTest.json") as f:
        punch_data = json.load(f)
    with open("BenefitLogicTest.json") as f:
        benefit_data = json.load(f)

    # Example: just sum the time punches as benefit total
    benefit_totals = {emp['employee']: {'benefitTotal': sum([1 for p in emp['timePunch']])}
                      for emp in punch_data['employeeData']}

    benefits, investments = calculate_benefits(benefit_totals, benefit_data, benefit_data)

    print("Benefit Allocations:\n", json.dumps(benefits, indent=2))
    print("Investment Allocations:\n", json.dumps(investments, indent=2))
