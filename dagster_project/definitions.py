"""Dagster code location for the tech test.

This directory is volume-mounted into the Dagster container, so changes are
picked up without rebuilding the image - use "Reload definitions" in the UI
(Deployment tab) after editing.

Register your asset, asset check, and schedule here. For example:

    from dagster_project.assets.sales_summary import (
        category_summary,
        category_summary_freshness_check,
        daily_category_summary_schedule,
    )

    defs = Definitions(
        assets=[category_summary],
        asset_checks=[category_summary_freshness_check],
        schedules=[daily_category_summary_schedule],
    )
"""

from dagster import Definitions

defs = Definitions(
    assets=[],
    asset_checks=[],
    schedules=[],
)
