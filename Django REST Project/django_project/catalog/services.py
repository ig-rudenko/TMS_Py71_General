from django.db.models import QuerySet
from django.db.transaction import atomic

from .models import Category, Product, Tag


def create_product(validated_data) -> Product:
    category_data = validated_data.pop("category")

    tags_data: list[str] = validated_data.pop("tags")

    with atomic():
        category, is_created = Category.objects.get_or_create(
            name=category_data["name"], defaults={"description": category_data.get("description", "")}
        )
        product = Product.objects.create(**validated_data, category=category)

        # TAGS
        new_tags_objs = []
        for tag_name in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            new_tags_objs.append(tag)

        product.tags.set(new_tags_objs)

    return product


def update_product(instance: Product, validated_data) -> Product:
    print("update_product", validated_data)

    tags_data: list[str] | None = validated_data.get("tags")
    if tags_data is not None:
        del validated_data["tags"]

    data = {**validated_data}

    with atomic():
        category_data = validated_data.get("category")
        if category_data is not None:
            category, is_created = Category.objects.get_or_create(
                name=category_data["name"], defaults={"description": category_data.get("description", "")}
            )
            data["category"] = category

        for attr, value in data.items():
            setattr(instance, attr, value)

        instance.save(update_fields=list(data.keys()))

        # TAGS
        if tags_data is not None:
            exists_tags_objs: QuerySet[Tag] = instance.tags.all()
            exists_tags_names = [tag.name for tag in exists_tags_objs]

            tags_to_remove = set(exists_tags_names) - set(tags_data)
            instance.tags.remove(*[tag for tag in exists_tags_objs if tag.name in tags_to_remove])

            new_tags_objs = []
            for tag_name in tags_data:
                if tag_name in exists_tags_names:
                    continue
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                new_tags_objs.append(tag)

            instance.tags.add(*new_tags_objs)

        return instance
