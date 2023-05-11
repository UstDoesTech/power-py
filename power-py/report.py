import requests
import json
import auth
import workspace

class Report:
    def __init__(self, report_name):
        self.report_name = report_name
        self.workspace_id = workspace.get_workspace_id(report_name)
        self.report_id = self.get_report_id(report_name)

    def get_report_id(self, report_name):
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/reports"
        header = auth.get_header()
        response = requests.get(url, headers=header)
        response_json = response.json()
        for report in response_json["value"]:
            if report["name"] == report_name:
                return report["id"]
            else:
                return None
            
    def get_report(self):
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/reports/{self.report_id}"
        header = auth.get_header()
        response = requests.get(url, headers=header)
        response_json = response.json()
        return response_json
    
    