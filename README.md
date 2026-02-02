# power-py

A Python SDK and CLI for Power BI and Microsoft Fabric APIs.

## Installation

```bash
pip install power-py
```

## Configuration

Set the following environment variables for authentication:

```bash
export POWERBI_CLIENT_ID="your-client-id"
export POWERBI_CLIENT_SECRET="your-client-secret"
export POWERBI_TENANT_ID="your-tenant-id"
```

## CLI Usage

The `power-py` CLI provides commands for managing Power BI and Microsoft Fabric resources.

### Power BI Commands

#### Workspaces

```bash
# List all workspaces
power-py workspace list

# Get workspace details
power-py workspace get <workspace_id>

# Create a new workspace
power-py workspace create "My Workspace"

# Delete a workspace
power-py workspace delete <workspace_id>

# List users in a workspace
power-py workspace users <workspace_id>

# Add a user to a workspace
power-py workspace add-user <workspace_id> user@example.com --role Admin --type User
```

#### Datasets

```bash
# List datasets in a workspace
power-py dataset list <workspace_id>

# Get dataset details
power-py dataset get <workspace_id> <dataset_id>

# Trigger a dataset refresh
power-py dataset refresh <workspace_id> <dataset_id>

# Get dataset refresh history
power-py dataset refresh-history <workspace_id> <dataset_id>

# List tables in a dataset
power-py dataset tables <workspace_id> <dataset_id>

# List datasources for a dataset
power-py dataset datasources <workspace_id> <dataset_id>
```

#### Reports

```bash
# List reports in a workspace
power-py report list <workspace_id>

# Get report details
power-py report get <workspace_id> <report_id>

# Clone a report
power-py report clone <workspace_id> <report_id> "New Report Name"

# Delete a report
power-py report delete <workspace_id> <report_id>

# Rebind a report to a different dataset
power-py report rebind <workspace_id> <report_id> <new_dataset_id>

# List pages in a report
power-py report pages <workspace_id> <report_id>
```

#### Dashboards

```bash
# List dashboards in a workspace
power-py dashboard list <workspace_id>

# Get dashboard details
power-py dashboard get <workspace_id> <dashboard_id>

# Create a new dashboard
power-py dashboard create <workspace_id> "My Dashboard"

# Delete a dashboard
power-py dashboard delete <workspace_id> <dashboard_id>

# List tiles in a dashboard
power-py dashboard tiles <workspace_id> <dashboard_id>
```

### Microsoft Fabric Commands

#### Fabric Workspaces

```bash
# List Fabric workspaces
power-py fabric workspace list

# Get Fabric workspace details
power-py fabric workspace get <workspace_id>

# Create a Fabric workspace
power-py fabric workspace create "My Workspace" --description "Description" --capacity-id <capacity_id>

# Delete a Fabric workspace
power-py fabric workspace delete <workspace_id>
```

#### Capacities

```bash
# List capacities
power-py fabric capacity list

# Get capacity details
power-py fabric capacity get <capacity_id>
```

#### Items

```bash
# List items in a workspace
power-py fabric item list <workspace_id>

# List items by type
power-py fabric item list <workspace_id> --type Lakehouse

# Get item details
power-py fabric item get <workspace_id> <item_id>

# Create a new item
power-py fabric item create <workspace_id> "My Item" Lakehouse

# Delete an item
power-py fabric item delete <workspace_id> <item_id>
```

#### Lakehouses

```bash
# List lakehouses
power-py fabric lakehouse list <workspace_id>

# Get lakehouse details
power-py fabric lakehouse get <workspace_id> <lakehouse_id>

# Create a lakehouse
power-py fabric lakehouse create <workspace_id> "My Lakehouse"

# Delete a lakehouse
power-py fabric lakehouse delete <workspace_id> <lakehouse_id>

# List tables in a lakehouse
power-py fabric lakehouse tables <workspace_id> <lakehouse_id>
```

#### Warehouses

```bash
# List warehouses
power-py fabric warehouse list <workspace_id>

# Get warehouse details
power-py fabric warehouse get <workspace_id> <warehouse_id>

# Create a warehouse
power-py fabric warehouse create <workspace_id> "My Warehouse"

# Delete a warehouse
power-py fabric warehouse delete <workspace_id> <warehouse_id>
```

#### Pipelines

```bash
# List pipelines
power-py fabric pipeline list <workspace_id>

# Get pipeline details
power-py fabric pipeline get <workspace_id> <pipeline_id>

# Run a pipeline
power-py fabric pipeline run <workspace_id> <pipeline_id>
```

#### Notebooks

```bash
# List notebooks
power-py fabric notebook list <workspace_id>

# Get notebook details
power-py fabric notebook get <workspace_id> <notebook_id>
```

#### Semantic Models

```bash
# List semantic models
power-py fabric semantic-model list <workspace_id>

# Get semantic model details
power-py fabric semantic-model get <workspace_id> <model_id>
```

## Python API Usage

You can also use the SDK programmatically:

```python
from power_py import Auth, Workspace, Dataset, Report, Dashboard, Fabric

# Initialize authentication
auth = Auth(
    client_id="your-client-id",
    client_secret="your-client-secret",
    authority="https://login.microsoftonline.com/your-tenant-id"
)

# Work with Power BI workspaces
workspace = Workspace(auth)
workspaces = workspace.list_workspaces()
print(workspaces)

# Work with datasets
workspace_id = "your-workspace-id"
dataset = Dataset(auth, workspace_id)
datasets = dataset.list_datasets()
print(datasets)

# Work with reports
report = Report(auth, workspace_id)
reports = report.list_reports()
print(reports)

# Work with dashboards
dashboard = Dashboard(auth, workspace_id)
dashboards = dashboard.list_dashboards()
print(dashboards)

# Work with Microsoft Fabric
fabric = Fabric(auth)
fabric_workspaces = fabric.list_workspaces()
lakehouses = fabric.list_lakehouses(workspace_id)
print(lakehouses)
```

## License

MIT License