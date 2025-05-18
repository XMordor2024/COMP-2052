from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.forms import TicketForm, UpdateTicketStatusForm
from app.models import db, Ticket, TicketCategory, User

# Blueprint principal que maneja el dashboard y la gestión de tickets
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Página de inicio pública (home).
    """
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    """
    Panel principal del usuario. Muestra los tickets creados por el usuario.
    """
    if current_user.role.name == 'Admin':
        tickets = Ticket.query.all()
    else:
        tickets = Ticket.query.filter_by(created_by=current_user).all()

    return render_template('dashboard.html', tickets=tickets)

@main.route('/tickets', methods=['GET', 'POST'])
@login_required
def crear_ticket():
    """
    Permite crear un nuevo ticket.
    """
    form = TicketForm()
    form.category.choices = [(c.id, c.name) for c in TicketCategory.query.all()]

    if form.validate_on_submit():
        category = TicketCategory.query.get(form.category.data)
        ticket = Ticket(
            title=form.title.data,
            description=form.description.data,
            category=category,
            created_by=current_user
        )
        db.session.add(ticket)
        db.session.commit()
        flash("Ticket created successfully.")
        return redirect(url_for('main.dashboard'))

    return render_template('ticket_form.html', form=form)

@main.route('/tickets/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_ticket(id):
    """
    Permite editar un ticket existente. Solo el creador o un admin puede editarlo.
    """
    ticket = Ticket.query.get_or_404(id)

    # Validación de permisos
    if current_user != ticket.created_by and current_user.role.name != 'Admin':
        flash('You do not have permission to edit this ticket.')
        return redirect(url_for('main.dashboard'))

    form = TicketForm(obj=ticket)
    form.category.choices = [(c.id, c.name) for c in TicketCategory.query.all()]

    if form.validate_on_submit():
        ticket.title = form.title.data
        ticket.description = form.description.data
        ticket.category = TicketCategory.query.get(form.category.data)
        db.session.commit()
        flash("Ticket updated successfully.")
        return redirect(url_for('main.dashboard'))

    return render_template('ticket_form.html', form=form, editar=True)

@main.route('/tickets/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_ticket(id):
    """
    Elimina un ticket si el usuario es admin o su creador.
    """
    ticket = Ticket.query.get_or_404(id)

    if current_user != ticket.created_by and current_user.role.name != 'Admin':
        flash('You do not have permission to delete this ticket.')
        return redirect(url_for('main.dashboard'))

    db.session.delete(ticket)
    db.session.commit()
    flash("Ticket deleted successfully.")
    return redirect(url_for('main.dashboard'))

@main.route('/tickets/<int:id>/actualizar_estado', methods=['GET', 'POST'])
@login_required
def actualizar_estado_ticket(id):
    """
    Permite actualizar el estado de un ticket. Solo admins o el creador pueden hacerlo.
    """
    ticket = Ticket.query.get_or_404(id)

    if current_user != ticket.created_by and current_user.role.name != 'Admin':
        flash('You do not have permission to update this ticket.')
        return redirect(url_for('main.dashboard'))

    form = UpdateTicketStatusForm(obj=ticket)

    if form.validate_on_submit():
        ticket.status = form.status.data
        db.session.commit()
        flash("Ticket status updated successfully.")
        return redirect(url_for('main.dashboard'))

    return render_template('update_ticket_status.html', form=form, ticket=ticket)