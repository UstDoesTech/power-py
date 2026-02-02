import requests


class Workspace:
    """Wrapper for Power BI Workspace API operations."""

    def __init__(self, auth, workspace_name=None):
        """
        Initialize a Workspace instance.

        Args:
            auth: An Auth instance for authentication.
            workspace_name: Optional workspace name. If provided, workspace_id will be fetched.
        """
        self.auth = auth
        self.workspace_name = workspace_name
        self.workspace_id = None
        if workspace_name:
            self.workspace_id = self.get_workspace_id()

    def get_workspace_id(self):
        """Get the workspace ID for the configured workspace name."""
        url = "https://api.powerbi.com/v1.0/myorg/groups"
        header = self.auth.get_header()
        response = requests.get(url, headers=header)
        response_json = response.json()
        for workspace in response_json.get("value", []):
            if workspace["name"] == self.workspace_name:
                return workspace["id"]
        return None

    def list_workspaces(self):
        """List all workspaces accessible to the authenticated user."""
        url = "https://api.powerbi.com/v1.0/myorg/groups"
        header = self.auth.get_header()
        response = requests.get(url, headers=header)
        response_json = response.json()
        return response_json.get("value", [])

    def get_workspace(self, workspace_id=None):
        """Get details of a specific workspace."""
        ws_id = workspace_id or self.workspace_id
        if not ws_id:
            raise ValueError("workspace_id is required")
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{ws_id}"
        header = self.auth.get_header()
        response = requests.get(url, headers=header)
        return response.json()

    def add_user(self, identifier, user_role, principal_type):
        """
        Add a user or service principal to the workspace.

        Args:
            identifier: Email address for users, or client ID for service principals.
            user_role: The role to assign (Admin, Contributor, Member, Viewer).
            principal_type: The type of principal (User, App, Group).
        """
        if not self.workspace_id:
            raise ValueError("workspace_id is required")
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}/users"
        header = self.auth.get_header()
        if principal_type.lower() == "app":
            payload = {
                "identifier": identifier,
                "groupUserAccessRight": user_role,
                "principalType": principal_type
            }
        elif principal_type.lower() == "user":
            payload = {
                "emailAddress": identifier,
                "groupUserAccessRight": user_role,
                "principalType": principal_type
            }
        else:
            payload = {
                "identifier": identifier,
                "groupUserAccessRight": user_role,
                "principalType": principal_type
            }
        response = requests.post(url, headers=header, json=payload)
        if response.status_code == 200:
            return {"status": "success"}
        return response.json()

    def create_workspace(self, workspace_name=None):
        """
        Create a new workspace.

        Args:
            workspace_name: Name of the workspace to create. Uses self.workspace_name if not provided.
        """
        name = workspace_name or self.workspace_name
        if not name:
            raise ValueError("workspace_name is required")
        url = "https://api.powerbi.com/v1.0/myorg/groups?workspaceV2=True"
        header = self.auth.get_header()
        payload = {"name": name}
        response = requests.post(url, headers=header, json=payload)
        return response.json()

    def delete_workspace(self, workspace_id=None):
        """Delete a workspace."""
        ws_id = workspace_id or self.workspace_id
        if not ws_id:
            raise ValueError("workspace_id is required")
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{ws_id}"
        header = self.auth.get_header()
        response = requests.delete(url, headers=header)
        if response.status_code == 200:
            return {"status": "success"}
        return response.json()

    def list_workspace_users(self, workspace_id=None):
        """List users in a workspace."""
        ws_id = workspace_id or self.workspace_id
        if not ws_id:
            raise ValueError("workspace_id is required")
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{ws_id}/users"
        header = self.auth.get_header()
        response = requests.get(url, headers=header)
        response_json = response.json()
        return response_json.get("value", [])
