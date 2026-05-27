from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Prediction(db.Model):
    __tablename__ = 'predictions'
    id         = db.Column(db.Integer, primary_key=True)
    fruit      = db.Column(db.String(50), nullable=False)
    verdict    = db.Column(db.String(30), nullable=False)
    fresh_pct  = db.Column(db.Float, nullable=False)
    filename   = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':         self.id,
            'fruit':      self.fruit,
            'verdict':    self.verdict,
            'fresh_pct':  self.fresh_pct,
            'created_at': self.created_at.strftime('%d %b %Y, %H:%M'),
        }
