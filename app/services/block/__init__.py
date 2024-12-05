from uuid import UUID

from fastapi import Depends
from app.models.block import Block, BlockSchema
from app.services import Service
from core.db.repository import DatabaseRepository
from core.fastapi.dependencies import get_repository


class BlockService(Service):
    async def create(self, user_id: UUID, block: dict) -> BlockSchema:
        try:
            async with self.uow as uow:
                data = await self.repo.create(
                    type=block["type"],
                    properties=block["properties"],
                    content=[str(i) for i in block["content"]],
                    parent=block["parent"],
                    user_id=user_id,
                )

                data = BlockSchema(
                    id=data.id,
                    type=data.type,
                    properties=data.properties,
                    content=data.content,
                    parent=data.parent,
                    user_id=user_id,
                )

                parent = await self.repo.get(
                    Block.id == data.parent, Block.user_id == data.user_id
                )

                content = parent.content + [str(data.id)]

                await self.repo.update(data.parent, {"content": content})

                await uow.commit()
        except Exception as e:
            raise e

        return data

    async def get(self, user_id: UUID, id: UUID) -> Block:
        try:
            data = await self.repo.get(Block.id == id, Block.user_id == user_id)
        except Exception as e:
            raise e

        return data

    async def update(self, user_id: UUID, id: UUID, data: dict) -> Block:
        try:
            block = await self.get(user_id, id)

            if block is None:
                raise ValueError

            if "content" in data:
                data["content"] = [str(i) for i in data["content"]]

            data = await self.repo.update(id, data)
        except Exception as e:
            raise e

        return BlockSchema(
            id=data.id,
            type=data.type,
            properties=data.properties,
            content=[str(i) for i in data.content],
            parent=data.parent,
            user_id=data.user_id,
        )

    async def delete(self, user_id: UUID, id: UUID) -> Block:
        try:
            async with self.uow as uow:
                block = await self.get(user_id, id)

                if block is None:
                    return {"message": "Block deleted successfully"}

                parent = await self.get(user_id, block.parent)

                content = [str(i) for i in parent.content if str(i) != str(id)]

                await self.repo.update(parent.id, {"content": content})

                await self.repo.delete(Block.id == id, Block.user_id == user_id)
        except Exception as e:
            raise e

        return {"message": "Block deleted successfully"}


def get_block_service():
    def func(repo: DatabaseRepository[Block] = Depends(get_repository(Block))):
        return BlockService(repo)

    return func
