from faker import Faker
from main import *
faker = Faker()
for _ in range(10):
    space = Space(space_name=faker.name(), space_description=faker.text())
    db.session.add(space)
    db.session.commit()
    for _ in range(10):
        category = Category(category_name=faker.name(), space_id=space.id)
        db.session.add(category)
        db.session.commit()
        for _ in range(10):
            subcategory = Subcategory(subcategory_name=faker.name(), parent_subcategory_id=category.id, parent_subcategory_name=category.category_name, category_id=category.id, category_name=category.category_name)
            db.session.add(subcategory)
            db.session.commit()
            for _ in range(10):
                url = Url(name=faker.name(), link=faker.url(), image=faker.image(), category_id=category.id, category_name=category.category_name, subcategory_id=subcategory.id, subcategory_name=subcategory.subcategory_name)
                db.session.add(url)
                db.session.commit()
                print(f"Added {url.name} to the database")
                print(f"Added {subcategory.subcategory_name} to the database")
                print(f"Added {category.category_name} to the database")
                print(f"Added {space.space_name} to the database")
                print(f"Added {space.space_description} to the database")
