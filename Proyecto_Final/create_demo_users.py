from app import create_app, db
from app.models import TicketCategory, Ticket, User

app = create_app()

with app.app_context():
    # Asegurarse de que las categorías de tickets existen
    categories = ['Bug', 'Feature Request', 'Support']
    for category_name in categories:
        existing_category = TicketCategory.query.filter_by(name=category_name).first()
        if not existing_category:
            new_category = TicketCategory(name=category_name)
            db.session.add(new_category)
            print(f'✅ Categoría "{category_name}" creada.')

    db.session.commit()

    # Diccionario con tickets a insertar
    tickets_data = [
        {
            "title": "Error en la página de inicio",
            "description": "La página de inicio no carga correctamente en dispositivos móviles.",
            "category_name": "Bug",
            "created_by_email": "admin@example.com"
        },
        {
            "title": "Agregar modo oscuro",
            "description": "Sería útil tener un modo oscuro para la aplicación.",
            "category_name": "Feature Request",
            "created_by_email": "prof@example.com"
        },
        {
            "title": "Problema con el inicio de sesión",
            "description": "No puedo iniciar sesión con mi cuenta registrada.",
            "category_name": "Support",
            "created_by_email": "student@example.com"
        }
    ]

    for ticket_info in tickets_data:
        existing_ticket = Ticket.query.filter_by(title=ticket_info['title']).first()
        if not existing_ticket:
            category = TicketCategory.query.filter_by(name=ticket_info['category_name']).first()
            created_by = User.query.filter_by(email=ticket_info['created_by_email']).first()
            if category and created_by:
                ticket = Ticket(
                    title=ticket_info['title'],
                    description=ticket_info['description'],
                    category=category,
                    created_by=created_by
                )
                db.session.add(ticket)
                print(f'✅ Ticket "{ticket.title}" creado en la categoría "{category.name}".')
            else:
                print(f'⚠️ No se pudo crear el ticket "{ticket_info["title"]}". Verifica la categoría o el usuario.')
        else:
            print(f'ℹ️ El ticket con título "{ticket_info["title"]}" ya existe.')

    db.session.commit()
    print("✅ Todos los tickets fueron procesados correctamente.")