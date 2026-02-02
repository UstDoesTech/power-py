import requests


class Report:
    """Wrapper for Power BI Report API operations."""

    def __init__(self, auth, workspace_id, report_name=None, report_id=None):
        """
        Initialize a Report instance.

        Args:
            auth: An Auth instance for authentication.
            workspace_id: The ID of the workspace containing the report.
            report_name: Optional report name. If provided, report_id will be fetched.
            report_id: Optional report ID. If provided, report_name lookup is skipped.
        """
        self.auth = auth
        self.workspace_id = workspace_id
        self.report_name = report_name
        self.report_id = report_id
        if report_name and not report_id:
            self.report_id = self.get_report_id()

    def list_reports(self):
        """List all reports in the workspace."""
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/reports"
        header = self.auth.get_header()
        response = requests.get(url, headers=header)
        response_json = response.json()
        return response_json.get("value", [])

    def get_report_id(self):
        """Get the report ID for the configured report name."""
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/reports"
        header = self.auth.get_header()
        response = requests.get(url, headers=header)
        response_json = response.json()
        for report in response_json.get("value", []):
            if report["name"] == self.report_name:
                return report["id"]
        return None

    def get_report(self, report_id=None):
        """Get details of a specific report."""
        rpt_id = report_id or self.report_id
        if not rpt_id:
            raise ValueError("report_id is required")
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/reports/{rpt_id}"
        header = self.auth.get_header()
        response = requests.get(url, headers=header)
        return response.json()

    def clone_report(self, name, target_workspace_id=None, target_dataset_id=None, report_id=None):
        """
        Clone a report.

        Args:
            name: Name of the cloned report.
            target_workspace_id: Target workspace ID. If not provided, clones to same workspace.
            target_dataset_id: Target dataset ID to rebind the cloned report.
            report_id: Source report ID. Uses self.report_id if not provided.
        """
        rpt_id = report_id or self.report_id
        if not rpt_id:
            raise ValueError("report_id is required")
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/reports/{rpt_id}/Clone"
        header = self.auth.get_header()
        payload = {"name": name}
        if target_workspace_id:
            payload["targetWorkspaceId"] = target_workspace_id
        if target_dataset_id:
            payload["targetModelId"] = target_dataset_id
        response = requests.post(url, headers=header, json=payload)
        return response.json()

    def export_report(self, report_id=None):
        """Export a report to .pbix format."""
        rpt_id = report_id or self.report_id
        if not rpt_id:
            raise ValueError("report_id is required")
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/reports/{rpt_id}/Export"
        header = self.auth.get_header()
        response = requests.get(url, headers=header)
        return response.content

    def delete_report(self, report_id=None):
        """Delete a report."""
        rpt_id = report_id or self.report_id
        if not rpt_id:
            raise ValueError("report_id is required")
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/reports/{rpt_id}"
        header = self.auth.get_header()
        response = requests.delete(url, headers=header)
        if response.status_code == 200:
            return {"status": "success"}
        return response.json()

    def rebind_report(self, dataset_id, report_id=None):
        """
        Rebind a report to a different dataset.

        Args:
            dataset_id: The ID of the dataset to rebind to.
            report_id: Report ID. Uses self.report_id if not provided.
        """
        rpt_id = report_id or self.report_id
        if not rpt_id:
            raise ValueError("report_id is required")
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/reports/{rpt_id}/Rebind"
        header = self.auth.get_header()
        payload = {"datasetId": dataset_id}
        response = requests.post(url, headers=header, json=payload)
        if response.status_code == 200:
            return {"status": "success"}
        return response.json()

    def get_pages(self, report_id=None):
        """Get pages in a report."""
        rpt_id = report_id or self.report_id
        if not rpt_id:
            raise ValueError("report_id is required")
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/reports/{rpt_id}/pages"
        header = self.auth.get_header()
        response = requests.get(url, headers=header)
        response_json = response.json()
        return response_json.get("value", [])
