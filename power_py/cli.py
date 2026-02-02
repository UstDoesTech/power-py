"""
Power BI and Fabric CLI - Command Line Interface for Power BI and Microsoft Fabric APIs.
"""
import click
import json
import os

from .src.auth import Auth
from .src.workspace import Workspace
from .src.dataset import Dataset
from .src.report import Report
from .src.dashboard import Dashboard
from .src.fabric import Fabric


def get_auth():
    """Get authentication instance from environment variables."""
    client_id = os.environ.get("POWERBI_CLIENT_ID")
    client_secret = os.environ.get("POWERBI_CLIENT_SECRET")
    tenant_id = os.environ.get("POWERBI_TENANT_ID")

    if not all([client_id, client_secret, tenant_id]):
        raise click.ClickException(
            "Missing required environment variables. Please set:\n"
            "  POWERBI_CLIENT_ID\n"
            "  POWERBI_CLIENT_SECRET\n"
            "  POWERBI_TENANT_ID"
        )

    authority = f"https://login.microsoftonline.com/{tenant_id}"
    return Auth(client_id, client_secret, authority)


def output_json(data, output_format="json"):
    """Output data in the specified format."""
    if output_format == "json":
        click.echo(json.dumps(data, indent=2))
    elif output_format == "table":
        if isinstance(data, list):
            if len(data) > 0:
                headers = data[0].keys()
                click.echo("\t".join(headers))
                click.echo("-" * 80)
                for item in data:
                    click.echo("\t".join(str(item.get(h, "")) for h in headers))
        else:
            for key, value in data.items():
                click.echo(f"{key}: {value}")


@click.group()
@click.version_option()
def cli():
    """Power BI and Fabric CLI - Manage Power BI and Microsoft Fabric resources."""
    pass


# =============================================================================
# Workspace Commands
# =============================================================================
@cli.group()
def workspace():
    """Manage Power BI workspaces."""
    pass


@workspace.command("list")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def workspace_list(output):
    """List all workspaces."""
    auth = get_auth()
    ws = Workspace(auth)
    workspaces = ws.list_workspaces()
    output_json(workspaces, output)


@workspace.command("get")
@click.argument("workspace_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def workspace_get(workspace_id, output):
    """Get details of a workspace."""
    auth = get_auth()
    ws = Workspace(auth)
    result = ws.get_workspace(workspace_id)
    output_json(result, output)


@workspace.command("create")
@click.argument("name")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def workspace_create(name, output):
    """Create a new workspace."""
    auth = get_auth()
    ws = Workspace(auth)
    result = ws.create_workspace(name)
    output_json(result, output)


@workspace.command("delete")
@click.argument("workspace_id")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
def workspace_delete(workspace_id, yes):
    """Delete a workspace."""
    if not yes:
        click.confirm(f"Are you sure you want to delete workspace {workspace_id}?", abort=True)
    auth = get_auth()
    ws = Workspace(auth)
    result = ws.delete_workspace(workspace_id)
    output_json(result)


@workspace.command("add-user")
@click.argument("workspace_id")
@click.argument("identifier")
@click.option("--role", "-r", type=click.Choice(["Admin", "Contributor", "Member", "Viewer"]),
              required=True, help="User role")
@click.option("--type", "-t", "principal_type",
              type=click.Choice(["User", "App", "Group"]), default="User",
              help="Principal type")
def workspace_add_user(workspace_id, identifier, role, principal_type):
    """Add a user or service principal to a workspace."""
    auth = get_auth()
    ws = Workspace(auth, workspace_name=None)
    ws.workspace_id = workspace_id
    result = ws.add_user(identifier, role, principal_type)
    output_json(result)


@workspace.command("users")
@click.argument("workspace_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def workspace_users(workspace_id, output):
    """List users in a workspace."""
    auth = get_auth()
    ws = Workspace(auth)
    users = ws.list_workspace_users(workspace_id)
    output_json(users, output)


# =============================================================================
# Dataset Commands
# =============================================================================
@cli.group()
def dataset():
    """Manage Power BI datasets."""
    pass


@dataset.command("list")
@click.argument("workspace_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def dataset_list(workspace_id, output):
    """List all datasets in a workspace."""
    auth = get_auth()
    ds = Dataset(auth, workspace_id)
    datasets = ds.list_datasets()
    output_json(datasets, output)


@dataset.command("get")
@click.argument("workspace_id")
@click.argument("dataset_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def dataset_get(workspace_id, dataset_id, output):
    """Get details of a dataset."""
    auth = get_auth()
    ds = Dataset(auth, workspace_id, dataset_id=dataset_id)
    result = ds.get_dataset()
    output_json(result, output)


@dataset.command("refresh")
@click.argument("workspace_id")
@click.argument("dataset_id")
def dataset_refresh(workspace_id, dataset_id):
    """Trigger a dataset refresh."""
    auth = get_auth()
    ds = Dataset(auth, workspace_id, dataset_id=dataset_id)
    result = ds.refresh_dataset()
    output_json(result)


@dataset.command("refresh-history")
@click.argument("workspace_id")
@click.argument("dataset_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def dataset_refresh_history(workspace_id, dataset_id, output):
    """Get refresh history of a dataset."""
    auth = get_auth()
    ds = Dataset(auth, workspace_id, dataset_id=dataset_id)
    history = ds.get_refresh_history()
    output_json(history, output)


@dataset.command("tables")
@click.argument("workspace_id")
@click.argument("dataset_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def dataset_tables(workspace_id, dataset_id, output):
    """List tables in a dataset."""
    auth = get_auth()
    ds = Dataset(auth, workspace_id, dataset_id=dataset_id)
    tables = ds.get_dataset_tables()
    output_json(tables, output)


@dataset.command("datasources")
@click.argument("workspace_id")
@click.argument("dataset_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def dataset_datasources(workspace_id, dataset_id, output):
    """List datasources for a dataset."""
    auth = get_auth()
    ds = Dataset(auth, workspace_id, dataset_id=dataset_id)
    datasources = ds.get_datasources()
    output_json(datasources, output)


# =============================================================================
# Report Commands
# =============================================================================
@cli.group()
def report():
    """Manage Power BI reports."""
    pass


@report.command("list")
@click.argument("workspace_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def report_list(workspace_id, output):
    """List all reports in a workspace."""
    auth = get_auth()
    rpt = Report(auth, workspace_id)
    reports = rpt.list_reports()
    output_json(reports, output)


@report.command("get")
@click.argument("workspace_id")
@click.argument("report_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def report_get(workspace_id, report_id, output):
    """Get details of a report."""
    auth = get_auth()
    rpt = Report(auth, workspace_id, report_id=report_id)
    result = rpt.get_report()
    output_json(result, output)


@report.command("clone")
@click.argument("workspace_id")
@click.argument("report_id")
@click.argument("name")
@click.option("--target-workspace", "-w", help="Target workspace ID")
@click.option("--target-dataset", "-d", help="Target dataset ID")
def report_clone(workspace_id, report_id, name, target_workspace, target_dataset):
    """Clone a report."""
    auth = get_auth()
    rpt = Report(auth, workspace_id, report_id=report_id)
    result = rpt.clone_report(name, target_workspace, target_dataset)
    output_json(result)


@report.command("delete")
@click.argument("workspace_id")
@click.argument("report_id")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
def report_delete(workspace_id, report_id, yes):
    """Delete a report."""
    if not yes:
        click.confirm(f"Are you sure you want to delete report {report_id}?", abort=True)
    auth = get_auth()
    rpt = Report(auth, workspace_id, report_id=report_id)
    result = rpt.delete_report()
    output_json(result)


@report.command("rebind")
@click.argument("workspace_id")
@click.argument("report_id")
@click.argument("dataset_id")
def report_rebind(workspace_id, report_id, dataset_id):
    """Rebind a report to a different dataset."""
    auth = get_auth()
    rpt = Report(auth, workspace_id, report_id=report_id)
    result = rpt.rebind_report(dataset_id)
    output_json(result)


@report.command("pages")
@click.argument("workspace_id")
@click.argument("report_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def report_pages(workspace_id, report_id, output):
    """List pages in a report."""
    auth = get_auth()
    rpt = Report(auth, workspace_id, report_id=report_id)
    pages = rpt.get_pages()
    output_json(pages, output)


# =============================================================================
# Dashboard Commands
# =============================================================================
@cli.group()
def dashboard():
    """Manage Power BI dashboards."""
    pass


@dashboard.command("list")
@click.argument("workspace_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def dashboard_list(workspace_id, output):
    """List all dashboards in a workspace."""
    auth = get_auth()
    db = Dashboard(auth, workspace_id)
    dashboards = db.list_dashboards()
    output_json(dashboards, output)


@dashboard.command("get")
@click.argument("workspace_id")
@click.argument("dashboard_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def dashboard_get(workspace_id, dashboard_id, output):
    """Get details of a dashboard."""
    auth = get_auth()
    db = Dashboard(auth, workspace_id, dashboard_id=dashboard_id)
    result = db.get_dashboard()
    output_json(result, output)


@dashboard.command("create")
@click.argument("workspace_id")
@click.argument("name")
def dashboard_create(workspace_id, name):
    """Create a new dashboard."""
    auth = get_auth()
    db = Dashboard(auth, workspace_id)
    result = db.add_dashboard(name)
    output_json(result)


@dashboard.command("delete")
@click.argument("workspace_id")
@click.argument("dashboard_id")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
def dashboard_delete(workspace_id, dashboard_id, yes):
    """Delete a dashboard."""
    if not yes:
        click.confirm(f"Are you sure you want to delete dashboard {dashboard_id}?", abort=True)
    auth = get_auth()
    db = Dashboard(auth, workspace_id, dashboard_id=dashboard_id)
    result = db.delete_dashboard()
    output_json(result)


@dashboard.command("tiles")
@click.argument("workspace_id")
@click.argument("dashboard_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def dashboard_tiles(workspace_id, dashboard_id, output):
    """List tiles in a dashboard."""
    auth = get_auth()
    db = Dashboard(auth, workspace_id, dashboard_id=dashboard_id)
    tiles = db.list_tiles()
    output_json(tiles, output)


# =============================================================================
# Fabric Commands
# =============================================================================
@cli.group()
def fabric():
    """Manage Microsoft Fabric resources."""
    pass


@fabric.group("workspace")
def fabric_workspace():
    """Manage Fabric workspaces."""
    pass


@fabric_workspace.command("list")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def fabric_workspace_list(output):
    """List all Fabric workspaces."""
    auth = get_auth()
    fab = Fabric(auth)
    workspaces = fab.list_workspaces()
    output_json(workspaces, output)


@fabric_workspace.command("get")
@click.argument("workspace_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def fabric_workspace_get(workspace_id, output):
    """Get details of a Fabric workspace."""
    auth = get_auth()
    fab = Fabric(auth)
    result = fab.get_workspace(workspace_id)
    output_json(result, output)


@fabric_workspace.command("create")
@click.argument("name")
@click.option("--description", "-d", help="Workspace description")
@click.option("--capacity-id", "-c", help="Capacity ID to assign")
def fabric_workspace_create(name, description, capacity_id):
    """Create a new Fabric workspace."""
    auth = get_auth()
    fab = Fabric(auth)
    result = fab.create_workspace(name, description, capacity_id)
    output_json(result)


@fabric_workspace.command("delete")
@click.argument("workspace_id")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
def fabric_workspace_delete(workspace_id, yes):
    """Delete a Fabric workspace."""
    if not yes:
        click.confirm(f"Are you sure you want to delete workspace {workspace_id}?", abort=True)
    auth = get_auth()
    fab = Fabric(auth)
    result = fab.delete_workspace(workspace_id)
    output_json(result)


@fabric.group("capacity")
def fabric_capacity():
    """Manage Fabric capacities."""
    pass


@fabric_capacity.command("list")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def fabric_capacity_list(output):
    """List all Fabric capacities."""
    auth = get_auth()
    fab = Fabric(auth)
    capacities = fab.list_capacities()
    output_json(capacities, output)


@fabric_capacity.command("get")
@click.argument("capacity_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def fabric_capacity_get(capacity_id, output):
    """Get details of a Fabric capacity."""
    auth = get_auth()
    fab = Fabric(auth)
    result = fab.get_capacity(capacity_id)
    output_json(result, output)


@fabric.group("item")
def fabric_item():
    """Manage Fabric items."""
    pass


@fabric_item.command("list")
@click.argument("workspace_id")
@click.option("--type", "-t", "item_type", help="Filter by item type")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def fabric_item_list(workspace_id, item_type, output):
    """List items in a Fabric workspace."""
    auth = get_auth()
    fab = Fabric(auth)
    items = fab.list_items(workspace_id, item_type)
    output_json(items, output)


@fabric_item.command("get")
@click.argument("workspace_id")
@click.argument("item_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def fabric_item_get(workspace_id, item_id, output):
    """Get details of a Fabric item."""
    auth = get_auth()
    fab = Fabric(auth)
    result = fab.get_item(workspace_id, item_id)
    output_json(result, output)


@fabric_item.command("create")
@click.argument("workspace_id")
@click.argument("name")
@click.argument("item_type")
@click.option("--description", "-d", help="Item description")
def fabric_item_create(workspace_id, name, item_type, description):
    """Create a new item in a Fabric workspace."""
    auth = get_auth()
    fab = Fabric(auth)
    result = fab.create_item(workspace_id, name, item_type, description)
    output_json(result)


@fabric_item.command("delete")
@click.argument("workspace_id")
@click.argument("item_id")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
def fabric_item_delete(workspace_id, item_id, yes):
    """Delete an item from a Fabric workspace."""
    if not yes:
        click.confirm(f"Are you sure you want to delete item {item_id}?", abort=True)
    auth = get_auth()
    fab = Fabric(auth)
    result = fab.delete_item(workspace_id, item_id)
    output_json(result)


@fabric.group("lakehouse")
def fabric_lakehouse():
    """Manage Fabric lakehouses."""
    pass


@fabric_lakehouse.command("list")
@click.argument("workspace_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def fabric_lakehouse_list(workspace_id, output):
    """List lakehouses in a Fabric workspace."""
    auth = get_auth()
    fab = Fabric(auth)
    lakehouses = fab.list_lakehouses(workspace_id)
    output_json(lakehouses, output)


@fabric_lakehouse.command("get")
@click.argument("workspace_id")
@click.argument("lakehouse_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def fabric_lakehouse_get(workspace_id, lakehouse_id, output):
    """Get details of a Fabric lakehouse."""
    auth = get_auth()
    fab = Fabric(auth)
    result = fab.get_lakehouse(workspace_id, lakehouse_id)
    output_json(result, output)


@fabric_lakehouse.command("create")
@click.argument("workspace_id")
@click.argument("name")
@click.option("--description", "-d", help="Lakehouse description")
def fabric_lakehouse_create(workspace_id, name, description):
    """Create a new lakehouse in a Fabric workspace."""
    auth = get_auth()
    fab = Fabric(auth)
    result = fab.create_lakehouse(workspace_id, name, description)
    output_json(result)


@fabric_lakehouse.command("delete")
@click.argument("workspace_id")
@click.argument("lakehouse_id")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
def fabric_lakehouse_delete(workspace_id, lakehouse_id, yes):
    """Delete a lakehouse from a Fabric workspace."""
    if not yes:
        click.confirm(f"Are you sure you want to delete lakehouse {lakehouse_id}?", abort=True)
    auth = get_auth()
    fab = Fabric(auth)
    result = fab.delete_lakehouse(workspace_id, lakehouse_id)
    output_json(result)


@fabric_lakehouse.command("tables")
@click.argument("workspace_id")
@click.argument("lakehouse_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def fabric_lakehouse_tables(workspace_id, lakehouse_id, output):
    """List tables in a Fabric lakehouse."""
    auth = get_auth()
    fab = Fabric(auth)
    tables = fab.list_lakehouse_tables(workspace_id, lakehouse_id)
    output_json(tables, output)


@fabric.group("warehouse")
def fabric_warehouse():
    """Manage Fabric warehouses."""
    pass


@fabric_warehouse.command("list")
@click.argument("workspace_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def fabric_warehouse_list(workspace_id, output):
    """List warehouses in a Fabric workspace."""
    auth = get_auth()
    fab = Fabric(auth)
    warehouses = fab.list_warehouses(workspace_id)
    output_json(warehouses, output)


@fabric_warehouse.command("get")
@click.argument("workspace_id")
@click.argument("warehouse_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def fabric_warehouse_get(workspace_id, warehouse_id, output):
    """Get details of a Fabric warehouse."""
    auth = get_auth()
    fab = Fabric(auth)
    result = fab.get_warehouse(workspace_id, warehouse_id)
    output_json(result, output)


@fabric_warehouse.command("create")
@click.argument("workspace_id")
@click.argument("name")
@click.option("--description", "-d", help="Warehouse description")
def fabric_warehouse_create(workspace_id, name, description):
    """Create a new warehouse in a Fabric workspace."""
    auth = get_auth()
    fab = Fabric(auth)
    result = fab.create_warehouse(workspace_id, name, description)
    output_json(result)


@fabric_warehouse.command("delete")
@click.argument("workspace_id")
@click.argument("warehouse_id")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
def fabric_warehouse_delete(workspace_id, warehouse_id, yes):
    """Delete a warehouse from a Fabric workspace."""
    if not yes:
        click.confirm(f"Are you sure you want to delete warehouse {warehouse_id}?", abort=True)
    auth = get_auth()
    fab = Fabric(auth)
    result = fab.delete_warehouse(workspace_id, warehouse_id)
    output_json(result)


@fabric.group("pipeline")
def fabric_pipeline():
    """Manage Fabric pipelines."""
    pass


@fabric_pipeline.command("list")
@click.argument("workspace_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def fabric_pipeline_list(workspace_id, output):
    """List pipelines in a Fabric workspace."""
    auth = get_auth()
    fab = Fabric(auth)
    pipelines = fab.list_pipelines(workspace_id)
    output_json(pipelines, output)


@fabric_pipeline.command("get")
@click.argument("workspace_id")
@click.argument("pipeline_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def fabric_pipeline_get(workspace_id, pipeline_id, output):
    """Get details of a Fabric pipeline."""
    auth = get_auth()
    fab = Fabric(auth)
    result = fab.get_pipeline(workspace_id, pipeline_id)
    output_json(result, output)


@fabric_pipeline.command("run")
@click.argument("workspace_id")
@click.argument("pipeline_id")
@click.option("--parameters", "-p", help="JSON string of pipeline parameters")
def fabric_pipeline_run(workspace_id, pipeline_id, parameters):
    """Run a Fabric pipeline."""
    auth = get_auth()
    fab = Fabric(auth)
    params = None
    if parameters:
        try:
            params = json.loads(parameters)
        except json.JSONDecodeError as e:
            raise click.ClickException(f"Invalid JSON for parameters: {e}")
    result = fab.run_pipeline(workspace_id, pipeline_id, params)
    output_json(result)


@fabric.group("notebook")
def fabric_notebook():
    """Manage Fabric notebooks."""
    pass


@fabric_notebook.command("list")
@click.argument("workspace_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def fabric_notebook_list(workspace_id, output):
    """List notebooks in a Fabric workspace."""
    auth = get_auth()
    fab = Fabric(auth)
    notebooks = fab.list_notebooks(workspace_id)
    output_json(notebooks, output)


@fabric_notebook.command("get")
@click.argument("workspace_id")
@click.argument("notebook_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def fabric_notebook_get(workspace_id, notebook_id, output):
    """Get details of a Fabric notebook."""
    auth = get_auth()
    fab = Fabric(auth)
    result = fab.get_notebook(workspace_id, notebook_id)
    output_json(result, output)


@fabric.group("semantic-model")
def fabric_semantic_model():
    """Manage Fabric semantic models."""
    pass


@fabric_semantic_model.command("list")
@click.argument("workspace_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def fabric_semantic_model_list(workspace_id, output):
    """List semantic models in a Fabric workspace."""
    auth = get_auth()
    fab = Fabric(auth)
    models = fab.list_semantic_models(workspace_id)
    output_json(models, output)


@fabric_semantic_model.command("get")
@click.argument("workspace_id")
@click.argument("model_id")
@click.option("--output", "-o", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def fabric_semantic_model_get(workspace_id, model_id, output):
    """Get details of a Fabric semantic model."""
    auth = get_auth()
    fab = Fabric(auth)
    result = fab.get_semantic_model(workspace_id, model_id)
    output_json(result, output)


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
