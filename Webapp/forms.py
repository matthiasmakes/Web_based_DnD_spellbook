from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, HiddenField, SelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from Webapp.models import SpellBooks, Spells


class RegistrationForm(FlaskForm):
    bookname = StringField("Book Name", validators=[DataRequired(),Length(min=3)])
    magicword = StringField("Magic Word", validators=[DataRequired(),Length(min=3)])
    magicword_confirm = StringField("Magic Word Confurmation", validators=[DataRequired(), EqualTo("magicword")])
    charator_class = SelectField("Class")
    charator_level = SelectField("Level", choices=list(range(1, 21)))
    submit = SubmitField("Make")


    def validate_bookname(self, bookname):
        book = SpellBooks.query.filter_by(name=bookname.data).first()
        if book:
            raise ValidationError('Spellbook name is in use, please pick another. ')



class OpenBook(FlaskForm):
    bookname = StringField("Book Name", validators=[DataRequired(), Length(min=3)])
    magicword = StringField("Magic Word", validators=[DataRequired(), Length(min=3)])
    remember = BooleanField("Remember me")
    submit = SubmitField("Open")


class SeachSpellsADV(FlaskForm):

    spellname = StringField("Spell name")
    spelllevel = SelectField("Level", choices=list(range(0, 21)))
    spellschool = SelectField("School")
    spellritual = BooleanField("Ritual")
    spellaction = SelectField("Action Type")
    spellrange = SelectField("Range")
    spellV = BooleanField("V")
    spellS = BooleanField("S")
    spellM = BooleanField("M")
    spellcomponent = BooleanField("Material")
    spellcaster = SelectMultipleField("Class")
    spellsource = SelectMultipleField("Source")
    spelldescription = StringField("Description")
    submit = SubmitField("Search")


class SeachSpells(FlaskForm):
    spellname = StringField("Spell name")
    submit = SubmitField("Open")

class addspell(FlaskForm):
    add = SubmitField("Add")
    spell_id = HiddenField()
    Check = BooleanField("add multiple")



class Startedit(FlaskForm):
    edit = SubmitField("edit")

class Editspellbook(FlaskForm):
    remove = SubmitField("Remove")
    spell_id = HiddenField()
    spelllevel = SelectField("Level", choices=list(range(0, 21)))

class Endedit(FlaskForm):
    done = SubmitField("Done")
    char_level = SelectField("Level", choices=list(range(1, 21)))
    char_mod = SelectField("Modifier", choices=list(range(-5, 11)))
    random = SubmitField("Random")
class Sort(FlaskForm):
    Sort = SubmitField("Sort")
    spellname = StringField("Spell name")
    level0 = BooleanField("0")
    level1 = BooleanField("1")
    level2 = BooleanField("2")
    level3 = BooleanField("3")
    level4 = BooleanField("4")
    level5 = BooleanField("5")
    level6 = BooleanField("6")
    level7 = BooleanField("7")
    level8 = BooleanField("8")
    level9 = BooleanField("9")


    spellschool = SelectField("School")
    spellritual = BooleanField("Ritual")
    spellaction = SelectField("Action Type")
    spellrange = SelectField("Range")
    spellV = BooleanField("V")
    spellS = BooleanField("S")
    spellM = BooleanField("M")
    spellcomponent = BooleanField("Material")
    spellcaster = SelectField("Class")
    spellsource = SelectField("Source")
    spelldescription = StringField("Description")