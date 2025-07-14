# challan_generator.py
# Creates a simple text-based e-challan file for a traffic violation

import os
from datetime import datetime

def generate_challan(plate_number, violation_type):
    """
    Generates a simple text-based e-challan with vehicle number and violation.
    Saves it to the /challans/ folder.
    """
    # Ensure challan folder exists
    os.makedirs("challans", exist_ok=True)

    # Generate a filename using plate and timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"challans/{plate_number}_{violation_type}_{timestamp}.txt"

    # Define challan content
    content = f"""
    E-CHALLAN

    Vehicle Number   : {plate_number}
    Violation Type   : {violation_type}
    Violation Time   : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    Fine Amount      : ₹500
    Officer ID       : TFC-{str(hash(plate_number))[-4:]}

    Note: This is an auto-generated challan. Please pay the fine within 7 days.
    """

    # Save to file
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content.strip())

    print(f"[INFO] Challan saved: {filename}")
