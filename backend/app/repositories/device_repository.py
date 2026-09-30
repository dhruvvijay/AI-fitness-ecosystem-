"""
Device repository — Bluetooth device CRUD and sync data.
"""

from typing import Optional, Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.repositories.base import BaseRepository
from app.models.social import Device, DeviceSyncData


class DeviceRepository(BaseRepository[Device]):
    def __init__(self, db: AsyncSession):
        super().__init__(Device, db)

    async def get_user_devices(self, user_id: int) -> Sequence[Device]:
        result = await self.db.execute(
            select(Device)
            .where(Device.user_id == user_id)
            .order_by(Device.created_at.desc())
        )
        return result.scalars().all()

    async def get_by_bluetooth_id(
        self, user_id: int, bluetooth_id: str
    ) -> Optional[Device]:
        result = await self.db.execute(
            select(Device).where(
                Device.user_id == user_id,
                Device.bluetooth_id == bluetooth_id,
            )
        )
        return result.scalar_one_or_none()

    async def add_sync_data(self, device_id: int, **kwargs) -> DeviceSyncData:
        data = DeviceSyncData(device_id=device_id, **kwargs)
        self.db.add(data)
        await self.db.flush()
        await self.db.refresh(data)
        return data

    async def get_recent_sync_data(
        self, device_id: int, limit: int = 100
    ) -> Sequence[DeviceSyncData]:
        result = await self.db.execute(
            select(DeviceSyncData)
            .where(DeviceSyncData.device_id == device_id)
            .order_by(DeviceSyncData.recorded_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
