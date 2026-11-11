import math

def parse_vitals_summary(vitals_csv):
    if not isinstance(vitals_csv, str):
        raise ValueError("Vitals input must be a string")

    parts = vitals_csv.split(',')
    if len(parts) != 3:
        raise ValueError("Vitals must have exactly 3 values: HR,SpO2,Temp")

    try:
        hr = float(parts[0])
        spo2 = float(parts[1])
        temp = float(parts[2])
    except ValueError:
        raise ValueError("Vitals values must be numbers")

    if not all(math.isfinite(v) for v in (hr, spo2, temp)):
        raise ValueError("Vitals values must be finite numbers")

    critical = hr > 120 or spo2 < 90 or temp > 39.0
    return f"Vitals: HR={hr}, SpO2={spo2}% - {'CRITICAL' if critical else 'STABLE'}"

def compute_patient_bmi(bmi_string):
    if not isinstance(bmi_string, str):
        raise ValueError("BMI input must be a string")

    parts = bmi_string.split('/')
    if len(parts) != 2:
        raise ValueError("BMI input must be in the form weight/height")

    try:
        weight = float(parts[0])
        height = float(parts[1])
    except ValueError:
        raise ValueError("Weight and height must be numbers")

    if not (math.isfinite(weight) and math.isfinite(height)):
        raise ValueError("Weight and height must be finite numbers")
    if weight <= 0 or height <= 0:
        raise ValueError("Weight and height must be greater than zero")

    try:
        bmi = weight / (height ** 2)
    except (ZeroDivisionError, OverflowError):
        raise ValueError("Height is outside the valid range")

    if not math.isfinite(bmi):
        raise ValueError("BMI result is not a finite number")

    return round(bmi, 2)

def assign_ward_bed(allocation_code):
    if not isinstance(allocation_code, str):
        raise ValueError("Allocation code must be a string")

    parts = allocation_code.strip().split('-')
    if len(parts) != 2:
        raise ValueError("Allocation code must be in the form WARD-BED")
    ward, bed_str = parts

    ward_names = {
        "ER": "Emergency Room",
        "ICU": "Intensive Care Unit",
        "GEN": "General Ward",
        "PED": "Pediatrics"
    }

    ward_key = ward.strip().upper()
    if ward_key not in ward_names:
        raise ValueError(f"Unknown ward: {ward}")

    try:
        bed_num = int(bed_str)
    except ValueError:
        raise ValueError("Bed number must be a whole number")

    if bed_num <= 0:
        raise ValueError("Bed number must be positive")

    return f"{ward_names[ward_key]} Bed #{bed_num}"

def main():
    print("==== Running parse_vitals_summary ====")
    v_input = input("Enter vitals (HR,SpO2,Temp): ")
    print("Summary:", parse_vitals_summary(v_input))

    print("\n==== Running compute_patient_bmi ====")
    b_input = input("Enter weight/height (e.g. 70/1.75): ")
    print("BMI:", compute_patient_bmi(b_input))

    print("\n==== Running assign_ward_bed ====")
    w_input = input("Enter allocation (e.g. ICU-05): ")
    print("Assignment:", assign_ward_bed(w_input))

if __name__ == "__main__":
    main()