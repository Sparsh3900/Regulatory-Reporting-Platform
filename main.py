from setup_database import setup_database
from validation import run_validation
from reporting import generate_monthly_report
from audit import detect_breach_and_log

def main():
    setup_database()

    if run_validation():
        report = generate_monthly_report()
        print("Monthly Report:")
        for row in report:
            print(row)

        detect_breach_and_log(report)
        print("Audit log updated.")

    else:
        print("Fix validation errors before reporting.")

if __name__ == "__main__":
    main()
