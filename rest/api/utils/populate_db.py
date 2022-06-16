from api import db
from api.models.user import User
from api.models.property import Property
from api.models.category import Category

import random


CATEGORIES = [
            ('Departamento','Propiedad dentro de un edificio de viviendas'),
            ('Loft','Vivienda o estudio adaptados a partir de una nave industrial.'),
            ('Casa','Inmueble destinadoa propiedad privada con un solo dueño'),
            ('Terreno','Extensión de tierra, especialmente cuando está delimitada por algo.'),
            ('Copropiedad','Inmueble destinadoa propiedad privada con mas de un dueño'),
            ('Local Comercial','Espacio físico donde se ofrecen bienes y servicios'),
            ('Contrato','Documento en que figura el derecho a habitar un inmueble, firmado por todas las partes.')]

def populate_users():
    for index in range(0,20):
        username = f"User_{index}"
        new_user = User(username,f"{username}@somemail.com")
        db.session.add(new_user)
        db.session.commit()

def populate_properties():
    streets = [
        'Batalla de Naco',
        'La otra banda',
        'Piedra del Comal',
        'Balcón de los edecanes',
        'Rayando el sol',
        'Barrio La Lonja',
        'Cerveza Noche Buena',
        'Tiro al pichón',
        'Calle de la Amargura',
        'Añejo de Bacardí',
        'Mar de la Crisis',
        'Maremoto',
        'Diablotitla',
        'Brandy Cheverny',
        'Lago de la Muerte',
        'Matapulgas',
        'Goma',
        'Salsipuedes',
        'Barranca del Muerto',
        'Lago de la Muerte',
        'Zopilote mojado'
    ]
    for street_name in streets:
        name = street_name + str(random.randint(10,100))
        category = Category.query.filter_by(name=random.choice(CATEGORIES)[0]).first()
        surface = random.randint(60,400)
        price = random.randint(600000,6000000)
        description = f"{category.name} en {street_name} de {surface} a ${price}"
        new_property = Property(name, description, price, surface, category.id)
        db.session.add(new_property)
        db.session.commit()

def populate_categories():
    for category in CATEGORIES:
        new_category = Category(category[0],category[1])
        db.session.add(new_category)
        db.session.commit()

