from app import create_app, db
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    inspector = inspect(db.engine)
    tablas = inspector.get_table_names()
    print("✅ Tablas creadas:", tablas)
    print("Cantidad:", len(tablas))