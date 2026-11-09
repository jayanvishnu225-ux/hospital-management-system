import os
import sys
import json
from pathlib import Path
from asgiref.sync import sync_to_async

PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Hms.settings")

import django
django.setup()

from mcp.server.fastmcp import FastMCP
from home.models import Doctor, booking, department

mcp = FastMCP("Hospital Management System")


@sync_to_async
def get_departments():
    return list(
        department.objects.order_by("department_name").values(
            "id",
            "department_name",
            "department_disc",
        )
    )


@sync_to_async
def get_doctors():
    return list(
        Doctor.objects.select_related("doc_dept")
        .order_by("doc_name")
        .values(
            "id",
            "doc_name",
            "doc_disc",
            "doc_spec",
            "doc_dept__department_name",
        )[:50]
    )


@sync_to_async
def get_appointment_count():
    return booking.objects.count()


@mcp.tool()
async def list_departments() -> str:
    """List hospital departments and their descriptions."""
    departments = await get_departments()
    return json.dumps(departments, ensure_ascii=False)


@mcp.tool()
async def list_doctors() -> str:
    """List up to 50 doctors, including their specialty and department."""
    doctors = await get_doctors()
    return json.dumps(doctors, ensure_ascii=False)


@mcp.tool()
async def count_appointments() -> str:
    """Count appointments without exposing patient information."""
    total = await get_appointment_count()
    return json.dumps({"total_appointments": total})


if __name__ == "__main__":
    mcp.run(transport="stdio")