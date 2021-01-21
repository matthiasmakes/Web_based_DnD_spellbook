from Webapp import db, login_manager
from flask_login import UserMixin
@login_manager.user_loader
def load_user(user_id):
    return SpellBooks.query.get(int(user_id))



class Spells(db.Model):
    __tablename__ = "Spells"
    ID = db.Column(db.Integer(), primary_key=True)
    Name = db.Column(db.String())
    Level = db.Column(db.Integer())
    School = db.Column(db.String())
    Ritual = db.Column(db.Boolean())
    Action_Type = db.Column(db.String())
    Range = db.Column(db.String())
    V_S_M = db.Column(db.String())
    Component = db.Column(db.Boolean())
    Caster = db.Column(db.String())
    Source = db.Column(db.String())
    Description = db.Column(db.String())

    def __repr__(self):
        return '<Name %r>' % self.ID


class SpellBooks(db.Model,UserMixin):
    __tablename__ = "SpellBooks"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    magic_word = db.Column(db.String())
    caster = db.Column(db.String())
    caster_modifier = db.Column(db.Integer())
    level = db.Column(db.Integer())
    spell_id = db.Column(db.String(), default="")



    def __repr__(self):
        return '<Name %r>' % self.ID
