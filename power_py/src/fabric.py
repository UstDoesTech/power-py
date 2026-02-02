import requests


class Fabric:
    """Wrapper for Microsoft Fabric REST API operations."""

    BASE_URL = "https://api.fabric.microsoft.com/v1"

    def __init__(self, auth):
        """
        Initialize a Fabric instance.

        Args:
            auth: An Auth instance for authentication (with Fabric scope).
        """
        self.auth = auth

    def _get_header(self):
        """Get authorization header for Fabric API calls."""
        access_token = self.auth.get_token()
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

    # Workspace Operations
    def list_workspaces(self):
        """List all Fabric workspaces."""
        url = f"{self.BASE_URL}/workspaces"
        response = requests.get(url, headers=self._get_header())
        response_json = response.json()
        return response_json.get("value", [])

    def get_workspace(self, workspace_id):
        """Get details of a specific workspace."""
        url = f"{self.BASE_URL}/workspaces/{workspace_id}"
        response = requests.get(url, headers=self._get_header())
        return response.json()

    def create_workspace(self, display_name, description=None, capacity_id=None):
        """
        Create a new Fabric workspace.

        Args:
            display_name: Display name of the workspace.
            description: Optional description.
            capacity_id: Optional capacity ID to assign the workspace.
        """
        url = f"{self.BASE_URL}/workspaces"
        payload = {"displayName": display_name}
        if description:
            payload["description"] = description
        if capacity_id:
            payload["capacityId"] = capacity_id
        response = requests.post(url, headers=self._get_header(), json=payload)
        return response.json()

    def delete_workspace(self, workspace_id):
        """Delete a Fabric workspace."""
        url = f"{self.BASE_URL}/workspaces/{workspace_id}"
        response = requests.delete(url, headers=self._get_header())
        if response.status_code == 200:
            return {"status": "success"}
        return response.json()

    def update_workspace(self, workspace_id, display_name=None, description=None):
        """Update a Fabric workspace."""
        url = f"{self.BASE_URL}/workspaces/{workspace_id}"
        payload = {}
        if display_name:
            payload["displayName"] = display_name
        if description:
            payload["description"] = description
        response = requests.patch(url, headers=self._get_header(), json=payload)
        if response.status_code == 200:
            return {"status": "success"}
        return response.json()

    # Capacity Operations
    def list_capacities(self):
        """List all capacities."""
        url = f"{self.BASE_URL}/capacities"
        response = requests.get(url, headers=self._get_header())
        response_json = response.json()
        return response_json.get("value", [])

    def get_capacity(self, capacity_id):
        """Get details of a specific capacity."""
        url = f"{self.BASE_URL}/capacities/{capacity_id}"
        response = requests.get(url, headers=self._get_header())
        return response.json()

    # Item Operations
    def list_items(self, workspace_id, item_type=None):
        """
        List items in a workspace.

        Args:
            workspace_id: The workspace ID.
            item_type: Optional item type filter (e.g., 'Lakehouse', 'Notebook', 'Warehouse').
        """
        url = f"{self.BASE_URL}/workspaces/{workspace_id}/items"
        if item_type:
            url += f"?type={item_type}"
        response = requests.get(url, headers=self._get_header())
        response_json = response.json()
        return response_json.get("value", [])

    def get_item(self, workspace_id, item_id):
        """Get details of a specific item."""
        url = f"{self.BASE_URL}/workspaces/{workspace_id}/items/{item_id}"
        response = requests.get(url, headers=self._get_header())
        return response.json()

    def create_item(self, workspace_id, display_name, item_type, description=None):
        """
        Create a new item in a workspace.

        Args:
            workspace_id: The workspace ID.
            display_name: Display name of the item.
            item_type: Type of item (e.g., 'Lakehouse', 'Notebook', 'Warehouse').
            description: Optional description.
        """
        url = f"{self.BASE_URL}/workspaces/{workspace_id}/items"
        payload = {
            "displayName": display_name,
            "type": item_type
        }
        if description:
            payload["description"] = description
        response = requests.post(url, headers=self._get_header(), json=payload)
        return response.json()

    def delete_item(self, workspace_id, item_id):
        """Delete an item from a workspace."""
        url = f"{self.BASE_URL}/workspaces/{workspace_id}/items/{item_id}"
        response = requests.delete(url, headers=self._get_header())
        if response.status_code == 200:
            return {"status": "success"}
        return response.json()

    def update_item(self, workspace_id, item_id, display_name=None, description=None):
        """Update an item in a workspace."""
        url = f"{self.BASE_URL}/workspaces/{workspace_id}/items/{item_id}"
        payload = {}
        if display_name:
            payload["displayName"] = display_name
        if description:
            payload["description"] = description
        response = requests.patch(url, headers=self._get_header(), json=payload)
        if response.status_code == 200:
            return {"status": "success"}
        return response.json()

    # Lakehouse Operations
    def list_lakehouses(self, workspace_id):
        """List all lakehouses in a workspace."""
        return self.list_items(workspace_id, item_type="Lakehouse")

    def get_lakehouse(self, workspace_id, lakehouse_id):
        """Get details of a specific lakehouse."""
        url = f"{self.BASE_URL}/workspaces/{workspace_id}/lakehouses/{lakehouse_id}"
        response = requests.get(url, headers=self._get_header())
        return response.json()

    def create_lakehouse(self, workspace_id, display_name, description=None):
        """Create a new lakehouse in a workspace."""
        url = f"{self.BASE_URL}/workspaces/{workspace_id}/lakehouses"
        payload = {"displayName": display_name}
        if description:
            payload["description"] = description
        response = requests.post(url, headers=self._get_header(), json=payload)
        return response.json()

    def delete_lakehouse(self, workspace_id, lakehouse_id):
        """Delete a lakehouse from a workspace."""
        url = f"{self.BASE_URL}/workspaces/{workspace_id}/lakehouses/{lakehouse_id}"
        response = requests.delete(url, headers=self._get_header())
        if response.status_code == 200:
            return {"status": "success"}
        return response.json()

    def list_lakehouse_tables(self, workspace_id, lakehouse_id):
        """List tables in a lakehouse."""
        url = f"{self.BASE_URL}/workspaces/{workspace_id}/lakehouses/{lakehouse_id}/tables"
        response = requests.get(url, headers=self._get_header())
        response_json = response.json()
        return response_json.get("value", [])

    def load_lakehouse_table(self, workspace_id, lakehouse_id, table_name, path_type,
                             relative_path, file_extension=None, format_options=None):
        """
        Load data into a lakehouse table.

        Args:
            workspace_id: The workspace ID.
            lakehouse_id: The lakehouse ID.
            table_name: Name of the table.
            path_type: Type of path ('File' or 'Folder').
            relative_path: Relative path to the data.
            file_extension: Optional file extension filter.
            format_options: Optional format options dictionary.
        """
        url = f"{self.BASE_URL}/workspaces/{workspace_id}/lakehouses/{lakehouse_id}/tables/{table_name}/load"
        payload = {
            "pathType": path_type,
            "relativePath": relative_path
        }
        if file_extension:
            payload["fileExtension"] = file_extension
        if format_options:
            payload["formatOptions"] = format_options
        response = requests.post(url, headers=self._get_header(), json=payload)
        if response.status_code == 202:
            return {"status": "load initiated"}
        return response.json()

    # Warehouse Operations
    def list_warehouses(self, workspace_id):
        """List all warehouses in a workspace."""
        return self.list_items(workspace_id, item_type="Warehouse")

    def get_warehouse(self, workspace_id, warehouse_id):
        """Get details of a specific warehouse."""
        url = f"{self.BASE_URL}/workspaces/{workspace_id}/warehouses/{warehouse_id}"
        response = requests.get(url, headers=self._get_header())
        return response.json()

    def create_warehouse(self, workspace_id, display_name, description=None):
        """Create a new warehouse in a workspace."""
        url = f"{self.BASE_URL}/workspaces/{workspace_id}/warehouses"
        payload = {"displayName": display_name}
        if description:
            payload["description"] = description
        response = requests.post(url, headers=self._get_header(), json=payload)
        return response.json()

    def delete_warehouse(self, workspace_id, warehouse_id):
        """Delete a warehouse from a workspace."""
        url = f"{self.BASE_URL}/workspaces/{workspace_id}/warehouses/{warehouse_id}"
        response = requests.delete(url, headers=self._get_header())
        if response.status_code == 200:
            return {"status": "success"}
        return response.json()

    # Notebook Operations
    def list_notebooks(self, workspace_id):
        """List all notebooks in a workspace."""
        return self.list_items(workspace_id, item_type="Notebook")

    def get_notebook(self, workspace_id, notebook_id):
        """Get details of a specific notebook."""
        url = f"{self.BASE_URL}/workspaces/{workspace_id}/notebooks/{notebook_id}"
        response = requests.get(url, headers=self._get_header())
        return response.json()

    # Pipeline Operations
    def list_pipelines(self, workspace_id):
        """List all pipelines in a workspace."""
        return self.list_items(workspace_id, item_type="DataPipeline")

    def get_pipeline(self, workspace_id, pipeline_id):
        """Get details of a specific pipeline."""
        url = f"{self.BASE_URL}/workspaces/{workspace_id}/dataPipelines/{pipeline_id}"
        response = requests.get(url, headers=self._get_header())
        return response.json()

    def run_pipeline(self, workspace_id, pipeline_id, parameters=None):
        """
        Run a pipeline.

        Args:
            workspace_id: The workspace ID.
            pipeline_id: The pipeline ID.
            parameters: Optional dictionary of pipeline parameters.
        """
        url = f"{self.BASE_URL}/workspaces/{workspace_id}/dataPipelines/{pipeline_id}/jobs/instances?jobType=Pipeline"
        payload = {}
        if parameters:
            payload["executionData"] = {"parameters": parameters}
        response = requests.post(url, headers=self._get_header(), json=payload if payload else None)
        if response.status_code == 202:
            return {"status": "run initiated"}
        return response.json()

    # Semantic Model Operations (Power BI Datasets in Fabric)
    def list_semantic_models(self, workspace_id):
        """List all semantic models in a workspace."""
        return self.list_items(workspace_id, item_type="SemanticModel")

    def get_semantic_model(self, workspace_id, semantic_model_id):
        """Get details of a specific semantic model."""
        url = f"{self.BASE_URL}/workspaces/{workspace_id}/semanticModels/{semantic_model_id}"
        response = requests.get(url, headers=self._get_header())
        return response.json()
