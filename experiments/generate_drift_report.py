import pandas as pd
import numpy as np
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import os
import http.server
import socketserver

# 1. Generate Mock Data
def get_mock_data():
    ref_data = pd.DataFrame({
        'confidence': np.random.normal(0.8, 0.1, 100),
        'class_id': np.random.randint(0, 38, 100)
    })
    curr_data = pd.DataFrame({
        'confidence': np.random.normal(0.6, 0.2, 100),
        'class_id': np.random.randint(0, 38, 100)
    })
    return ref_data, curr_data

print("Generating Data Drift Report...")
reference, current = get_mock_data()

# 2. Create Report (Using Old API)
dashboard = Dashboard(tabs=[DataDriftTab()])
dashboard.calculate(reference, current)

# 3. Save to HTML
output_dir = "monitoring_reports"
os.makedirs(output_dir, exist_ok=True)
report_path = os.path.join(output_dir, "index.html")
dashboard.save(report_path)

print(f"Report saved to {report_path}")

# 4. Serve on Port 7000
PORT = 7000
DIRECTORY = output_dir

class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        return super().translate_path(path).replace(os.getcwd(), os.path.join(os.getcwd(), DIRECTORY))

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Evidently Dashboard running at http://localhost:{PORT}")
    httpd.serve_forever()