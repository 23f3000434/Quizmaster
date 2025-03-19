import click
from flask.cli import with_appcontext
from datetime import date
from quizmaster import db, bcrypt
from quizmaster.models import User

def init_db():
    db.create_all()

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

@click.command('create-admin')
@with_appcontext
def create_admin():
    """Create admin user"""
    admin = User.query.filter_by(Email='admin@quizmaster.com').first()
    if admin:
        click.echo('Admin already exists')
        return
    
    hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
    admin = User(
        Full_Name='Admin',
        Email='admin@quizmaster.com',
        Qualification='Admin',
        Password=hashed_password,
        dob=date.today(),
        is_admin=True
    )
    db.session.add(admin)
    db.session.commit()
    click.echo('Admin created successfully')