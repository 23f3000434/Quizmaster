import click
from flask.cli import with_appcontext
from quizmaster import db, bcrypt
from quizmaster.models import User
from datetime import date

@click.command(name='create-admin')
@click.argument('email')
@click.argument('password')
@click.option('--name', default='Admin User', help='Full name for the admin')
@with_appcontext
def create_admin(email, password, name):
    """Create a new admin user"""
    existing_user = User.query.filter_by(Email=email).first()
    
    if existing_user:
        if existing_user.is_admin:
            click.echo(f'User {email} is already an admin!')
            return
        else:
            existing_user.is_admin = True
            db.session.commit()
            click.echo(f'User {email} has been upgraded to admin!')
            
            return
        
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(
        Full_Name = name,
        Email = email,
        Qualification = Administrator,
        Password = hashed_password,
        dob = date.today(),
        is_admin = True
    )
    db.session.add(user)
    db.session.commit()
    click.echo(f'Admin user {email} created successfully!')