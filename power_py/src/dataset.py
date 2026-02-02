import requests
import json


class Dataset:
    """Wrapper for Power BI Dataset API operations."""

    def __init__(self, auth, workspace_id, dataset_name=None, dataset_id=None):
        """
        Initialize a Dataset instance.

        Args:
            auth: An Auth instance for authentication.
            workspace_id: The ID of the workspace containing the dataset.
            dataset_name: Optional dataset name. If provided, dataset_id will be fetched.
            dataset_id: Optional dataset ID. If provided, dataset_name lookup is skipped.
        """
        self.auth = auth
        self.workspace_id = workspace_id
        self.dataset_name = dataset_name
        self.dataset_id = dataset_id
        if dataset_name and not dataset_id:
            self.dataset_id = self.get_dataset_id()

    def list_datasets(self):
        """List all datasets in the workspace."""
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/datasets"
        header = self.auth.get_header()
        response = requests.get(url, headers=header)
        response_json = response.json()
        return response_json.get("value", [])

    def get_dataset_id(self):
        """Get the dataset ID for the configured dataset name."""
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/datasets"
        header = self.auth.get_header()
        response = requests.get(url, headers=header)
        response_json = response.json()
        for dataset in response_json.get("value", []):
            if dataset["name"] == self.dataset_name:
                return dataset["id"]
        return None

    def get_dataset(self, dataset_id=None):
        """Get details of a specific dataset."""
        ds_id = dataset_id or self.dataset_id
        if not ds_id:
            raise ValueError("dataset_id is required")
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/datasets/{ds_id}"
        header = self.auth.get_header()
        response = requests.get(url, headers=header)
        return response.json()

    def get_dataset_tables(self, dataset_id=None):
        """Get tables in a dataset."""
        ds_id = dataset_id or self.dataset_id
        if not ds_id:
            raise ValueError("dataset_id is required")
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/datasets/{ds_id}/tables"
        header = self.auth.get_header()
        response = requests.get(url, headers=header)
        return response.json()

    def get_dataset_table(self, table_name, dataset_id=None):
        """Get a specific table in a dataset."""
        ds_id = dataset_id or self.dataset_id
        if not ds_id:
            raise ValueError("dataset_id is required")
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/datasets/{ds_id}/tables/{table_name}"
        header = self.auth.get_header()
        response = requests.get(url, headers=header)
        return response.json()

    def refresh_dataset(self, dataset_id=None):
        """Trigger a refresh of the dataset."""
        ds_id = dataset_id or self.dataset_id
        if not ds_id:
            raise ValueError("dataset_id is required")
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/datasets/{ds_id}/refreshes"
        header = self.auth.get_header()
        response = requests.post(url, headers=header)
        if response.status_code == 202:
            return {"status": "refresh triggered"}
        return response.json()

    def get_refresh_history(self, dataset_id=None):
        """Get the refresh history of a dataset."""
        ds_id = dataset_id or self.dataset_id
        if not ds_id:
            raise ValueError("dataset_id is required")
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/datasets/{ds_id}/refreshes"
        header = self.auth.get_header()
        response = requests.get(url, headers=header)
        response_json = response.json()
        return response_json.get("value", [])

    def update_storage_mode(self, storage_mode, dataset_id=None):
        """
        Update the storage mode of a dataset.

        Args:
            storage_mode: The target storage mode (e.g., 'PremiumFiles', 'Abf').
            dataset_id: Optional dataset ID. Uses self.dataset_id if not provided.
        """
        ds_id = dataset_id or self.dataset_id
        if not ds_id:
            raise ValueError("dataset_id is required")
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/datasets/{ds_id}"
        header = self.auth.get_header()
        data = {"targetStorageMode": storage_mode}
        response = requests.patch(url, headers=header, data=json.dumps(data))
        if response.status_code == 200:
            return {"status": "success"}
        return response.json()

    def get_datasources(self, dataset_id=None):
        """Get the datasources for a dataset."""
        ds_id = dataset_id or self.dataset_id
        if not ds_id:
            raise ValueError("dataset_id is required")
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/datasets/{ds_id}/datasources"
        header = self.auth.get_header()
        response = requests.get(url, headers=header)
        response_json = response.json()
        return response_json.get("value", [])
