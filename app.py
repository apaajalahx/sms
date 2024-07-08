from src import init_app, db

flask = init_app('development')

@flask.cli.command('migrate:fresh')
def migrate_fresh():
    """ Migration Fresh Database """
    with flask.app_context():
        db.create_all()

@flask.cli.command('migrate:drop')
def migrate_drop():
    """ Drop All Database """
    with flask.app_context():
        db.drop_all()

if __name__ == '__main__':
    flask.run('0.0.0.0', 3000)