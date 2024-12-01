import click
from flask.cli import with_appcontext
from app import db
from app.models import User  # Import all your models

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    db.drop_all()
    db.create_all()
    click.echo('Initialized the database.')

@click.command('seed-db')
@with_appcontext
def seed_db_command():
    """Seed the database with some initial data."""
    # Create a test user
    test_user = User(username='test_user')
    test_user.set_password('password123')
    db.session.add(test_user)
    
    try:
        db.session.commit()
        click.echo('Database seeded.')
    except Exception as e:
        db.session.rollback()
        click.echo(f'Error seeding database: {str(e)}')