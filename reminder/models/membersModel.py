from extensions import db

class Member(db.Model):
    __tablename__ = 'members'

    memberid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    wa_number = db.Column(db.String(80), unique=True, nullable=False)
    dob = db.Column(db.Date)
    accepted_terms = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return f'<Member {self.memberid}>'
        