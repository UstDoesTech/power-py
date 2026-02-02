import requests


class Dashboard:
    """Wrapper for Power BI Dashboard API operations."""

    def __init__(self, auth, workspace_id, dashboard_name=None, dashboard_id=None):
        """
        Initialize a Dashboard instance.

        Args:
            auth: An Auth instance for authentication.
            workspace_id: The ID of the workspace containing the dashboard.
            dashboard_name: Optional dashboard name. If provided, dashboard_id will be fetched.
            dashboard_id: Optional dashboard ID. If provided, dashboard_name lookup is skipped.
        """
        self.auth = auth
        self.workspace_id = workspace_id
        self.dashboard_name = dashboard_name
        self.dashboard_id = dashboard_id
        if dashboard_name and not dashboard_id:
            self.dashboard_id = self.get_dashboard_id()

    def list_dashboards(self):
        """List all dashboards in the workspace."""
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/dashboards"
        header = self.auth.get_header()
        response = requests.get(url, headers=header)
        response_json = response.json()
        return response_json.get("value", [])

    def get_dashboard_id(self):
        """Get the dashboard ID for the configured dashboard name."""
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/dashboards"
        header = self.auth.get_header()
        response = requests.get(url, headers=header)
        response_json = response.json()
        for dashboard in response_json.get("value", []):
            if dashboard["displayName"] == self.dashboard_name:
                return dashboard["id"]
        return None

    def get_dashboard(self, dashboard_id=None):
        """Get details of a specific dashboard."""
        db_id = dashboard_id or self.dashboard_id
        if not db_id:
            raise ValueError("dashboard_id is required")
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/dashboards/{db_id}"
        header = self.auth.get_header()
        response = requests.get(url, headers=header)
        return response.json()

    def list_tiles(self, dashboard_id=None):
        """List tiles in a dashboard."""
        db_id = dashboard_id or self.dashboard_id
        if not db_id:
            raise ValueError("dashboard_id is required")
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/dashboards/{db_id}/tiles"
        header = self.auth.get_header()
        response = requests.get(url, headers=header)
        response_json = response.json()
        return response_json.get("value", [])

    def get_tile(self, tile_id, dashboard_id=None):
        """Get a specific tile in a dashboard."""
        db_id = dashboard_id or self.dashboard_id
        if not db_id:
            raise ValueError("dashboard_id is required")
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/dashboards/{db_id}/tiles/{tile_id}"
        header = self.auth.get_header()
        response = requests.get(url, headers=header)
        return response.json()

    def clone_tile(self, tile_id, target_dashboard_id, target_workspace_id=None,
                   target_report_id=None, target_dataset_id=None, dashboard_id=None):
        """
        Clone a tile to another dashboard.

        Args:
            tile_id: The source tile ID.
            target_dashboard_id: The target dashboard ID.
            target_workspace_id: Optional target workspace ID.
            target_report_id: Optional target report ID.
            target_dataset_id: Optional target dataset ID.
            dashboard_id: Source dashboard ID. Uses self.dashboard_id if not provided.
        """
        db_id = dashboard_id or self.dashboard_id
        if not db_id:
            raise ValueError("dashboard_id is required")
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/dashboards/{db_id}/tiles/{tile_id}/Clone"
        header = self.auth.get_header()
        payload = {"targetDashboardId": target_dashboard_id}
        if target_workspace_id:
            payload["targetWorkspaceId"] = target_workspace_id
        if target_report_id:
            payload["targetReportId"] = target_report_id
        if target_dataset_id:
            payload["targetModelId"] = target_dataset_id
        response = requests.post(url, headers=header, json=payload)
        return response.json()

    def add_dashboard(self, dashboard_name=None):
        """
        Create a new dashboard in the workspace.

        Args:
            dashboard_name: Name of the dashboard. Uses self.dashboard_name if not provided.
        """
        name = dashboard_name or self.dashboard_name
        if not name:
            raise ValueError("dashboard_name is required")
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/dashboards"
        header = self.auth.get_header()
        payload = {"name": name}
        response = requests.post(url, headers=header, json=payload)
        return response.json()

    def delete_dashboard(self, dashboard_id=None):
        """Delete a dashboard."""
        db_id = dashboard_id or self.dashboard_id
        if not db_id:
            raise ValueError("dashboard_id is required")
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/dashboards/{db_id}"
        header = self.auth.get_header()
        response = requests.delete(url, headers=header)
        if response.status_code == 200:
            return {"status": "success"}
        return response.json()
