from data_sources.sqlalchemy import db


class TotalMobile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20))

    def __repr__(self):
        return f"Reference: {self.reference}, Status: {self.status}"
