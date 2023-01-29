from extensions import db

class Record(db.Model):
    __tablename__ = 'records'
    recordid = db.Column(db.Integer, primary_key=True)
    memberid = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    updated_on = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return f'<Record {self.recordid}>'