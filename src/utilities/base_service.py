from tortoise import Model
from typing import Type, List, Optional
from src.error.base import ErrorHandler


class BaseObjectService:
    def __init__(self, model: Type[Model]):
        self.model = model
        self.error = ErrorHandler(self.model)

    async def get_object_or_404(self, **kwargs):
        return await self.model.filter(is_deleted=False, **kwargs).first()

    async def filter_object(self, **kwargs):
        return await self.model.filter(is_deleted=False, **kwargs).all()

    async def all(
        self,
        prefetch_related: Optional[List[str]] = None,
        select_related: Optional[List[str]] = None,
        page: int = 1,
        count: int = 10
    ):
        offset = (page - 1) * count
        query = self.model.filter(is_deleted=False)

        if select_related:
            query = query.select_related(*select_related)
        if prefetch_related:
            query = query.prefetch_related(*prefetch_related)
        total = await query.count()
        query = query.offset(offset).limit(count)
        results = await query.all()
        return {
            "page": page,
            "page_size": count,
            "total": total,
            "results": results,
        }


    async def trash(self, id: str):
        obj = await self.model.filter(id=id, is_deleted=False).first()
        if not obj:
            return None
        obj.is_deleted = True
        await obj.save()
        return obj

    async def delete(self, id: str):
        obj = await self.model.filter(id=id).first()
        if not obj:
            return None
        await obj.delete()
        return True

    async def recover(self, ids: List[str]):
        objs = await self.model.filter(id__in=ids, is_deleted=True).all()
        for obj in objs:
            obj.is_deleted = False
            await obj.save()
        return objs

    async def bulk_trash(self, ids: List[str]):
        objs = await self.model.filter(id__in=ids, is_deleted=False).all()
        for obj in objs:
            obj.is_deleted = True
            await obj.save()
        return objs

    async def bulk_delete(self, ids: List[str]):
        objs = await self.model.filter(id__in=ids).all()
        for obj in objs:
            await obj.delete()
        return True
