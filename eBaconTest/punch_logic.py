import json

from datetime import datetime

def calculate_hours(start, end):
    fmt = "%Y-%m-%d %H:%M:%S"
    s = datetime.strptime(start, fmt)
    e = datetime.strptime(end, fmt)
    delta = e - s
    return delta.total_seconds() / 3600

def load_json(file_path):
    with open(file_path) as f:
        return json.load(f)

def calculate_pay(employee_data, job_meta):
    results = {}
    for emp in employee_data:
        total_hours = 0
        wage_total = 0
        benefit_total = 0
        for punch in emp['timePunch']:
            job_info = next((j for j in job_meta if j['job'] == punch['job']), None)
            if not job_info:
                continue
            hours = calculate_hours(punch['start'], punch['end'])
            regular = min(max(40 - total_hours, 0), hours)
            overtime = min(max(total_hours + hours - 40, 0), 8 if total_hours < 48 else 0)
            doubletime = max(total_hours + hours - 48, 0) if total_hours > 48 else 0
            wage_total += regular * job_info['rate'] + overtime * job_info['rate'] * 1.5 + doubletime * job_info['rate'] * 2
            benefit_total += hours * job_info['benefitsRate']
            total_hours += hours
        results[emp['employee']] = {
            'employee': emp['employee'],
            'regular': round(min(total_hours, 40), 4),
            'overtime': round(max(total_hours - 40, 0), 4),
            'doubletime': round(max(total_hours - 48, 0), 4),
            'wageTotal': round(wage_total, 4),
            'benefitTotal': round(benefit_total, 4)
        }
    return results

if __name__ == "__main__":
    data = load_json("PunchLogicTest.json")
    output = calculate_pay(data['employeeData'], data['jobMeta'])
    print(json.dumps(output, indent=2))
