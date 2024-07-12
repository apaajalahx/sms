from src import init_app, db
import os

app = init_app(os.getenv('APP_ENV'))

@app.cli.command('migrate:fresh')
def migrate_fresh():
    """ Migration Fresh Database """
    with app.app_context():
        db.create_all()

@app.cli.command('migrate:drop')
def migrate_drop():
    """ Drop All Database """
    with app.app_context():
        db.drop_all()

if __name__ == '__main__':
    app.run('0.0.0.0', 3000)