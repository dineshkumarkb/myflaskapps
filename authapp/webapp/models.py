from authapp.webapp import db
from sqlalchemy.dialects.postgresql import UUID


class Details(db.Model):
    name = db.Column(db.String(255))
    id = db.Column(UUID(as_uuid=True), primary_key=True)