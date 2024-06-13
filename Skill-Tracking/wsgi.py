from app import create_app
from app.models import connect_db

app = create_app()
app.secret_key = 'cooperwashere'
connect_db(app)

