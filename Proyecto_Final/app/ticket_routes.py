from flask import Blueprint, request, jsonify
from app.models import db, Ticket, TicketCategory, User

# Blueprint solo con endpoints de prueba para tickets
main = Blueprint('main', __name__)

@main.route('/')  # Ambas rutas llevan al mismo lugar
@main.route('/dashboard')
def index():
    """
    Página de inicio pública (home).
    """
    return '<h1>Corriendo en Modo de Prueba para Tickets.</h1>'

@main.route('/tickets', methods=['GET'])
def listar_tickets():
    """
    Retorna una lista de tickets (JSON).
    """
    tickets = Ticket.query.all()

    data = [
        {
            'id': ticket.id,
            'title': ticket.title,
            'description': ticket.description,
            'status': ticket.status,
            'category': ticket.category.name,
            'created_by': ticket.created_by.username
        }
        for ticket in tickets
    ]
    return jsonify(data), 200

@main.route('/tickets/<int:id>', methods=['GET'])
def listar_un_ticket(id):
    """
    Retorna un solo ticket por su ID (JSON).
    """
    ticket = Ticket.query.get_or_404(id)

    data = {
        'id': ticket.id,
        'title': ticket.title,
        'description': ticket.description,
        'status': ticket.status,
        'category': ticket.category.name,
        'created_by': ticket.created_by.username
    }

    return jsonify(data), 200

@main.route('/tickets', methods=['POST'])
def crear_ticket():
    """
    Crea un ticket sin validación.
    Espera JSON con 'title', 'description', 'category_id' y 'created_by_id'.
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    category = TicketCategory.query.get(data.get('category_id'))
    user = User.query.get(data.get('created_by_id'))

    if not category or not user:
        return jsonify({'error': 'Invalid category or user ID'}), 400

    ticket = Ticket(
        title=data.get('title'),
        description=data.get('description'),
        status='Open',
        category=category,
        created_by=user
    )

    db.session.add(ticket)
    db.session.commit()

    return jsonify({'message': 'Ticket creado', 'id': ticket.id}), 201

@main.route('/tickets/<int:id>', methods=['PUT'])
def actualizar_ticket(id):
    """
    Actualiza un ticket sin validación de usuario o permisos.
    """
    ticket = Ticket.query.get_or_404(id)
    data = request.get_json()

    ticket.title = data.get('title', ticket.title)
    ticket.description = data.get('description', ticket.description)
    ticket.status = data.get('status', ticket.status)

    if 'category_id' in data:
        category = TicketCategory.query.get(data.get('category_id'))
        if category:
            ticket.category = category

    db.session.commit()

    return jsonify({'message': 'Ticket actualizado', 'id': ticket.id}), 200

@main.route('/tickets/<int:id>', methods=['DELETE'])
def eliminar_ticket(id):
    """
    Elimina un ticket sin validación de permisos.
    """
    ticket = Ticket.query.get_or_404(id)
    db.session.delete(ticket)
    db.session.commit()

    return jsonify({'message': 'Ticket eliminado', 'id': ticket.id}), 200