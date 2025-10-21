from src.utilities.base_service import BaseObjectService
from src.apps.public.blog import Blog, Category
from src.error.base import ErrorHandler
from src.enums.base import ContentStatus
from src.apps.auth.user import User
from slugify import slugify
from src.apps.file import File
from src.apps.public.blog.schemas import CategorySchema, BlogSchema




class CategoryService:
    error = ErrorHandler(Category)
    boa = BaseObjectService(Category)


    @classmethod
    async def create(cls, user: User, dto: CategorySchema):
        print(user)
        return await cls.boa.model.create(**dto.dict(exclude_unset=True), added_by=user)
       
    

    @classmethod
    async def all(cls, page: int = 1, count: int = 10):
        data = await cls.boa.all(select_related=["added_by"], page=page, count=count)
        
        results = []
        for cat in data["results"]:
            results.append({
                "id": str(cat.id),
                "title": cat.title,
                "slug": cat.slug,
                "added_by": f"{cat.added_by.first_name} {cat.added_by.last_name}" if cat.added_by else None,
                "created_at": cat.created_at,
                "updated_at": cat.updated_at
            })

        return {
            "page": data["page"],
            "page_size": data["page_size"],
            "total": data["total"],
            "results": results,
        }

    

    @classmethod
    async def get(cls, id: str):
        return await cls.boa.get_object_or_404(id=id)
    

    @classmethod
    async def update(cls, id: str, dto: CategorySchema):
        category = await cls.boa.get_object_or_404(id=id)
        if not category:
            raise ValueError("Category not found")
        data = dto.dict(exclude_unset=True, exclude={"added_by"})
        for field, value in data.items():
            setattr(category, field, value)
        if "title" in data and data["title"]:
            category.slug = slugify(data["title"])
        return await category.save()
    

    @classmethod
    async def delete(cls, id: str):
        return await cls.boa.delete(id=id)
 
class BlogService:
    error = ErrorHandler(Blog)
    boa = BaseObjectService(Blog)
    file = BaseObjectService(File)

    @classmethod
    async def create(cls, user: User, dto: BlogSchema):
        blog = cls.boa.model(**dto.dict(exclude={"author"}))
        blog.author = user
        await blog.save()  

        if dto.image_ids:
            for image_id in dto.image_ids:
                image = await cls.file.model.get_or_none(id=image_id)
                if image:
                    await blog.images.add(image)
        return blog

       


    @classmethod
    async def all(cls, author: str | None = None, category: str | None = None, page: int = 1, count: int = 10):
        query = cls.boa.model.filter(
            is_deleted=False,
            status=ContentStatus.PUBLISH
        ).select_related("author", "category").prefetch_related("images")  # M2M

        if author:
            query = query.filter(
                author__first_name__icontains=author
            ) | query.filter(
                author__last_name__icontains=author
            )

        if category:
            query = query.filter(category__title__icontains=category)

        total = await query.count()
        offset = (page - 1) * count
        query = query.offset(offset).limit(count)
        blogs = await query.all()

        results = []
        for blog in blogs:
            results.append({
                "id": str(blog.id),
                "title": blog.title,
                "slug": blog.slug,
                "content": blog.content,
                "status": blog.status,
                "category": blog.category.title if blog.category else None,
                "author": f"{blog.author.first_name} {blog.author.last_name}" if blog.author else None,
                "images": [image.url for image in blog.images],
                "tags": blog.tags, 
                "views_count": blog.views_count,
                "created_at": blog.created_at,
                "updated_at": blog.updated_at,
            })

        return {
            "page": page,
            "page_size": count,
            "total": total,
            "data": results,
        }


    @classmethod
    async def get(cls, id: str):
        return await cls.boa.get_object_or_404(id=id)

    @classmethod
    async def update(cls, id: str, dto: BlogSchema):
        blog = await cls.boa.get_object_or_404(id=id)
        if not blog:
            raise cls.error.get(404, "Blog not found")

        data = dto.dict(exclude_unset=True, exclude={"author"})
        for field, value in data.items():
            setattr(blog, field, value)

        if "title" in data and data["title"]:
            blog.slug = slugify(data["title"])

        return await blog.save()

    @classmethod
    async def delete(cls, id: str):
        return await cls.boa.delete(id=id)