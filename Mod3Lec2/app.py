from init import create_app, db
from model import User, Role
from werkzeug.security import generate_password_hash

app = create_app()

@app.before_request
def crear_tablas():
    db.create_all()
    if not Role.query.filter_by(name='admin').first():
        db.session.add(Role(name='admin'))
    if not Role.query.filter_by(name='user').first():
        db.session.add(Role(name='user'))
    db.session.commit()
    
    if not User.query.filter_by(username='admin1').first():
        admin_role = Role.query.filter_by(name='admin').first()
        db.session.add(User(username='admin1',
                            password=generate_password_hash('admin123'),
                            role=admin_role))
    if not User.query.filter_by(username='user1').first():
        user_role = Role.query.filter_by(name='user').first()
        db.session.add(User(username='user1',
                            password=generate_password_hash('user123'),
                            role=user_role))
    db.session.commit()
    
if __name__ == '__main__':
    app.run(debug=True)