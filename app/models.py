from . import db

### Models
class Action(db.Model):

    __tablename__ = 'action'

    id = db.Column(db.Integer, primary_key=True)
    logType = db.Column(db.String(20), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("user", uselist=False))
    sessionId = db.Column(db.String(100), nullable=False)
    properties = db.Column(db.JSON, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, logType: str, userId: int, sessionId: int, properties: str, date: str):
        self.logType = logType
        self.userId = userId
        self.sessionId = sessionId
        self.properties = properties
        self.date = date

class User(db.Model):
    # TODO: Add password, email, names, and other user-related attributes 
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)

    def __init__(self, username: str):
        self.username = username