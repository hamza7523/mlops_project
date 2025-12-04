import os
import http.server
import socketserver
import numpy as np
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

# 1. Load Real Class Names (Your Dataset)
try:
    # Try reading from root or current dir
    if os.path.exists("class_names.txt"):
        with open("class_names.txt", "r") as f:
            class_names = [line.strip() for line in f.readlines() if line.strip()]
    elif os.path.exists("../class_names.txt"):
        with open("../class_names.txt", "r") as f:
            class_names = [line.strip() for line in f.readlines() if line.strip()]
    else:
        # Fallback if file not moved during build
        class_names = [f"Disease_Class_{i}" for i in range(38)]
    
    print(f"✅ Loaded {len(class_names)} classes from class_names.txt")

except Exception as e:
    print(f"⚠️ Could not load class names: {e}")
    class_names = [f"Disease_Class_{i}" for i in range(38)]

# 2. Generate Realistic Data Simulation
# Reference: Represents your balanced Training Data
ref_size = 1000
reference_data = pd.DataFrame({
    "prediction": np.random.choice(class_names, size=ref_size),
    "confidence": np.random.uniform(0.7, 0.99, size=ref_size),
})

# Current: Represents Production Data (With Drift!)
# Simulate a drift where the first class is appearing too often
curr_size = 500
current_drift = np.random.choice(class_names, size=curr_size)

# Force 30% of data to be one specific disease to show "Drift" in the report
drift_class = class_names[0] if class_names else "Drifted_Class"
current_drift[:150] = drift_class 

current_data = pd.DataFrame({
    "prediction": current_drift,
    "confidence": np.random.uniform(0.5, 0.95, size=curr_size),
})

print("Generating Data Drift Report on Plant Disease Classes...")

# 3. Create the Report (Compatible with Evidently 0.4.0)
report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=reference_data, current_data=current_data)

# 4. Save to HTML
output_dir = "monitoring_reports"
os.makedirs(output_dir, exist_ok=True)
report_path = os.path.join(output_dir, "index.html")
report.save_html(report_path)

print(f"Report saved to {report_path}")

# 5. Serve on Port 7000
PORT = 7000
DIRECTORY = output_dir

class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        target = super().translate_path(path)
        return target.replace(os.getcwd(), os.path.join(os.getcwd(), DIRECTORY))

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Evidently Dashboard running at http://localhost:{PORT}")
    httpd.serve_forever()
