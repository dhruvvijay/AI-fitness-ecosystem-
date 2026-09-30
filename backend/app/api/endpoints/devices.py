"""
Devices API — Bluetooth device management and sync.
"""

from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.repositories.device_repository import DeviceRepository
from app.core.exceptions import NotFoundException
from app.core.responses import success_response

router = APIRouter(prefix="/devices", tags=["Devices"])


class RegisterDeviceRequest(BaseModel):
    device_name: str
    device_type: str  # fitness_band, smart_watch, heart_rate, scale, step_counter
    bluetooth_id: Optional[str] = None
    firmware_version: Optional[str] = None

class SyncDataRequest(BaseModel):
    sync_type: str  # heart_rate, steps, calories, sleep
    value: float
    unit: Optional[str] = None


@router.get("")
async def get_devices(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all user devices."""
    repo = DeviceRepository(db)
    devices = await repo.get_user_devices(user.id)
    return success_response(data=[
        {
            "id": d.id,
            "device_name": d.device_name,
            "device_type": d.device_type,
            "bluetooth_id": d.bluetooth_id,
            "is_connected": d.is_connected,
            "battery_level": d.battery_level,
            "last_sync_at": d.last_sync_at.isoformat() if d.last_sync_at else None,
        }
        for d in devices
    ])


@router.post("")
async def register_device(
    body: RegisterDeviceRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Register a new Bluetooth device."""
    repo = DeviceRepository(db)
    # Check duplicate
    if body.bluetooth_id:
        existing = await repo.get_by_bluetooth_id(user.id, body.bluetooth_id)
        if existing:
            return success_response(data={"id": existing.id}, message="Device already registered")

    device = await repo.create(
        user_id=user.id, device_name=body.device_name,
        device_type=body.device_type, bluetooth_id=body.bluetooth_id,
        firmware_version=body.firmware_version,
    )
    return success_response(data={"id": device.id, "device_name": device.device_name}, message="Device registered")


@router.post("/{device_id}/sync")
async def sync_device_data(
    device_id: int,
    body: SyncDataRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Sync data from a device."""
    repo = DeviceRepository(db)
    device = await repo.get_by_id(device_id)
    if not device or device.user_id != user.id:
        raise NotFoundException("Device", device_id)

    await repo.add_sync_data(
        device_id=device_id,
        sync_type=body.sync_type,
        value=body.value,
        unit=body.unit,
        recorded_at=datetime.now(timezone.utc),
    )

    # Update last sync timestamp
    device.last_sync_at = datetime.now(timezone.utc)
    await db.flush()

    return success_response(message="Data synced")


@router.delete("/{device_id}")
async def remove_device(
    device_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Remove a device."""
    repo = DeviceRepository(db)
    device = await repo.get_by_id(device_id)
    if not device or device.user_id != user.id:
        raise NotFoundException("Device", device_id)
    await repo.delete_by_id(device_id)
    return success_response(message="Device removed")
