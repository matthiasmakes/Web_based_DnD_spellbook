from flask import *
from Webapp.models import Spells, SpellBooks
from Webapp.forms import *
from Webapp import app, db
from flask_login import login_user, current_user, logout_user, login_required
from Webapp.method import *
from random import *


# make model
@app.route('/')
def home():

    return render_template("home.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    spellcaster = Spells.query.with_entities(Spells.Caster).distinct()
    caster_set = set()
    for var in spellcaster:
        caster_set.update(var)
    bigstring = str()
    for string in caster_set:
        bigstring = bigstring + string + ",\u2002"
    casterlist = bigstring.split(",\u2002")
    caster_set.clear()
    caster_set = set(casterlist)
    caster_set.remove('')

    # make book
    form = RegistrationForm()

    form.charator_class.choices = seleclist(caster_set)
    if form.validate_on_submit():
        spellBook = SpellBooks(name=form.bookname.data, magic_word=form.magicword.data, caster=form.charator_class.data,
                               level=form.charator_level.data)
        db.session.add(spellBook)
        db.session.commit()
        flash(f'Book {form.bookname.data} was greatet! you can now login', "success")
        return redirect(url_for("login"))
    return render_template("register.html", tittle="Register", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = OpenBook()
    if form.validate_on_submit():
        spellbook = SpellBooks.query.filter_by(name=form.bookname.data).first()
        if spellbook and spellbook.magic_word == form.magicword.data:
            login_user(spellbook, remember=form.remember.data)
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for("home"))
        else:
            flash("You are not login , wrong book or magicword")
    return render_template("login.html", form=form)


@app.route("/spell", methods=['GET', 'POST'])
def spell_by_name():
    # init  the spellist

    spellname = safe_input(request.form.get("name"))
    spelllevel = safe_input(request.form.get("level"))
    if spelllevel == "":
        query_level = ""
    else:
        query_level = ", Spells.Level == spelllevel"

    spellschool = safe_input(request.form.get("school"))
    spellritual = safe_input(request.form.get("ritual"))
    if spellritual == "on":
        spellritual = True
        query_ritual = ",Spells.Ritual == spellritual"
    else:
        spellritual = False
        query_ritual = ""
    spellaction = safe_input(request.form.get("action_type"))
    spellrange = safe_input(request.form.get("range"))

    spellV = safe_input(request.form.get("v"))
    if spellV == "on":
        spellV = "V"

    else:
        spellV = ""

    spellS = safe_input(request.form.get("s"))
    if spellS == "on":
        spellS = "S"
    else:
        spellS = ""

    spellM = safe_input(request.form.get("m"))
    if spellM == "on":
        spellM = "M"
    else:
        spellM = ""
    spellcomponent = safe_input(request.form.get("component"))
    if spellcomponent == "on":
        spellcomponent = True
        query_component = ", Spells.Component == spellcomponent"
    else:
        spellcomponent = False
        query_component = ""
    spellcaster = safe_input(request.form.get("caster"))
    spellsource = safe_input(request.form.get("source"))

    spelldescription = safe_input(request.form.get("description"))

    # stop init

    # makes the qury
    function_string = "Spells.query.filter("
    query_base = "Spells.Name.ilike(('%' + spellname + '%')),Spells.Range.ilike(('%' + spellrange + '%')),Spells.Caster.ilike(('%' + spellcaster + '%')), Spells.School.ilike(('%' + spellschool + '%')),Spells.Action_Type.ilike(('%' + spellaction + '%')),Spells.V_S_M.ilike(('%' + spellV + '%' + '%' + spellS + '%' + '%' + spellM + '%')),Spells.Description.ilike(('%' + spelldescription + '%'))"
    function_end = ").all()"

    spell_list = eval(function_string + query_base + query_level + query_ritual + query_component + function_end)

    # makes the form
    form = addspell()
    if form.validate_on_submit():
        spell_id = form.spell_id.data
        current_user.spell_id = current_user.spell_id + "," + spell_id
        db.session.add(current_user)
        db.session.commit()
    a = list()
    len(a)

    return render_template("spell.html", spelllist=spell_list, debug="", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/book", methods=['GET', 'POST'])
@login_required
def book():
    formsort = Sort(request.args)
    spell_from_db = list()
    spelllist = str(current_user.spell_id).split(",")
    try:
        spelllist.remove("")
    except:
        pass
    for spell in spelllist:
        spell_from_db.append(Spells.query.get(spell))
    levels = list()
    tempspelllist = list()
    if formsort.level0.data:
        levels.append(0)
    if formsort.level1.data:
        levels.append(1)
    if formsort.level2.data:
        levels.append(2)
    if formsort.level3.data:
        levels.append(3)
    if formsort.level4.data:
        levels.append(4)
    if formsort.level5.data:
        levels.append(5)
    if formsort.level6.data:
        levels.append(6)
    if formsort.level7.data:
        levels.append(7)
    if formsort.level8.data:
        levels.append(8)
    if formsort.level9.data:
        levels.append(9)

    spell_from_db = spell_quick_sort(spell_from_db)

    if not levels.__len__() == 0:
        for spells in spell_from_db:
            if spells.Level in levels:
                tempspelllist.append(spells)
        spell_from_db = tempspelllist




    return render_template("book.html", tittle="Book", spelllist=spell_from_db, formsort=formsort )


@app.route("/edit", methods=['GET', 'POST'])
@login_required
def edit():
    form = Endedit()
    form.char_level.default = current_user.level
    form.char_mod.default = current_user.caster_modifier
    form.process()
    form2 = Editspellbook()
    formsort = Sort(request.args)
    spell_from_db = list()
    spell_id = None
    if current_user.is_authenticated:
        spelllist = str(current_user.spell_id).split(",")
        try:
            spelllist.remove("")
        except:
            pass
        for spell in spelllist:
            spell_from_db.append(Spells.query.get(spell))

    if form.random.raw_data:
        levl = int(form.char_level.raw_data[0])
        caster = current_user.caster
        modifier = int(form.char_mod.raw_data[0])
        max_spells = levl + modifier
        if max_spells <= 0:
            max_spells = 1
        max_spell_lvl = int(levl / 1.5)
        if max_spell_lvl >= 10:
            max_spell_lvl = 9
        potential_spells = Spells.query.filter(Spells.Level < max_spell_lvl+1).all()
        new_spell_lst = list()
        for i in range(0, max_spells):
            r = randrange(0, potential_spells.__len__())
            new_spell_lst.append(potential_spells.pop(r))
        id_lst = list()
        for spell in new_spell_lst:
            id_lst.append(spell.ID)
        current_user.spell_id = list_to_string(id_lst)
        db.session.add(current_user)
        db.session.commit()







    if form.done.raw_data:

        current_user.level = form.char_level.raw_data[0]
        current_user.caster_modifier = form.char_mod.raw_data[0]
        db.session.add(current_user)
        db.session.commit()
        flash("book updated")
        return  redirect(url_for("book"))


    if form2.remove.data:
        spell_id = form2.spell_id.raw_data[1]
        newSpellList = str(current_user.spell_id).split(",")
        newSpellList.remove(spell_id)
        current_user.spell_id = list_to_string(newSpellList)
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for("edit"))

    levels = list()
    tempspelllist = list()
    if formsort.level0.data:
        levels.append(0)
    if formsort.level1.data:
        levels.append(1)
    if formsort.level2.data:
        levels.append(2)
    if formsort.level3.data:
        levels.append(3)
    if formsort.level4.data:
        levels.append(4)
    if formsort.level5.data:
        levels.append(5)
    if formsort.level6.data:
        levels.append(6)
    if formsort.level7.data:
        levels.append(7)
    if formsort.level8.data:
        levels.append(8)
    if formsort.level9.data:
        levels.append(9)

    spell_from_db = spell_quick_sort(spell_from_db)

    if not levels.__len__() == 0:
        for spells in spell_from_db:
            if spells.Level in levels:
                tempspelllist.append(spells)
        spell_from_db = tempspelllist



    return render_template("edit.html", spelllist=spell_from_db, form1=form, form2=form2, formsort=formsort, debug1 = current_user.level)



@app.route("/search", methods=['GET', 'POST'])
def search():
    form = SeachSpellsADV(request.args)
    form2 = addspell()
    newSpellList = None
    spell_id = None
    spell_school = Spells.query.with_entities(Spells.School).distinct()
    school_set = set()
    for spells in spell_school:
        school_set.update(spells)
    school_set = sorted(school_set)

    spellrange = Spells.query.with_entities(Spells.Range).distinct()
    spellrange_set = set()
    for spells in spellrange:
        spellrange_set.update(spells)
    spellrange_set = sorted(spellrange_set)

    spellaction = Spells.query.with_entities(Spells.Action_Type).distinct()
    spellaction_set = set()
    for spells in spellaction:
        spellaction_set.update(spells)
    spellaction_set = sorted(spellaction_set)

    spellcaster = Spells.query.with_entities(Spells.Caster).distinct()
    caster_set = set()
    for var in spellcaster:
        caster_set.update(var)
    bigstring = str()
    for string in caster_set:
        bigstring = bigstring + string + ",\u2002"
    casterlist = bigstring.split(",\u2002")
    caster_set.clear()
    caster_set = set(casterlist)
    caster_set.remove('')

    spellsource = Spells.query.with_entities(Spells.Source).distinct()
    spellsource_set = set()
    for spells in spellsource:
        spellsource_set.update(spells)
    spellsource_set = sorted(spellsource_set)

    form.spelllevel.choices.insert(0, '')
    form.spellschool.choices = seleclist(school_set)
    form.spellschool.choices.insert(0, ('', ''))
    form.spellrange.choices = seleclist(spellrange_set)
    form.spellrange.choices.insert(0, ('', ''))
    form.spellaction.choices = seleclist(spellaction_set)
    form.spellaction.choices.insert(0, ('', ''))
    form.spellcaster.choices = seleclist(caster_set)
    form.spellcaster.choices.insert(0, ('', ''))
    form.spellsource.choices = seleclist(spellsource_set)

    spell_list = None

    if form.validate():

        # init  the spellist

        spellname = safe_input(form.spellname.data)
        spelllevel = safe_input(form.spelllevel.data)
        if spelllevel == "":
            query_level = ""
        else:
            query_level = ", Spells.Level == spelllevel"

        spellschool = safe_input(form.spellschool.data)
        spellritual = form.spellritual.data
        if spellritual:
            query_ritual = ",Spells.Ritual == spellritual"
        else:
            query_ritual = ""
        spellaction = safe_input(form.spellaction.data)
        spellrange = safe_input(form.spellrange.data)

        spellV = form.spellV.data
        if spellV:
            spellV = "V"

        else:
            spellV = ""

        spellS = form.spellS.data
        if spellS:
            spellS = "S"
        else:
            spellS = ""

        spellM = form.spellM.data
        if spellM:
            spellM = "M"
        else:
            spellM = ""
        spellcomponent = form.spellcomponent.data
        if spellcomponent:
            query_component = ", Spells.Component == spellcomponent"
        else:
            query_component = ""
        spellcaster = safe_input_list(form.spellcaster.data)
        spellsource = safe_input_list(form.spellsource.data)

        spelldescription = safe_input(form.spelldescription.data)



        # stop init

        # makes the qury
        function_string = "Spells.query.filter("
        query_base = "Spells.Name.ilike(('%' + spellname + '%')),Spells.Range.ilike(('%' + spellrange + '%')), Spells.School.ilike(('%' + spellschool + '%')),Spells.Action_Type.ilike(('%' + spellaction + '%')),Spells.V_S_M.ilike(('%' + spellV + '%' + '%' + spellS + '%' + '%' + spellM + '%')),Spells.Description.ilike(('%' + spelldescription + '%'))"
        # OC query_base = "Spells.Name.ilike(('%' + spellname + '%')),Spells.Range.ilike(('%' + spellrange + '%')),Spells.Caster.ilike(('%' + spellcaster + '%')), Spells.School.ilike(('%' + spellschool + '%')),Spells.Action_Type.ilike(('%' + spellaction + '%')),Spells.V_S_M.ilike(('%' + spellV + '%' + '%' + spellS + '%' + '%' + spellM + '%')),Spells.Description.ilike(('%' + spelldescription + '%'))"
        function_end = ").all()"
        temp = function_string + query_base + query_level + query_ritual + query_component+ Multicaster_ilike(spellcaster) + function_end
        spell_list = eval(function_string + query_base + query_level + query_ritual + query_component+ Multicaster_ilike(spellcaster) + SpellsSource_ilike(spellsource) + function_end)


    if form2.validate_on_submit():
        if current_user.is_authenticated:
            newSpellList = set(str(current_user.spell_id).split(","))
            newSpellList.add(form2.spell_id.data)
            try:
                newSpellList.remove("")
            except:
                pass
            current_user.spell_id = list_to_string(newSpellList)
            db.session.add(current_user)
            db.session.commit()
    return render_template("search.html", tittle="search", form=form, form2=form2, spelllist=spell_list,
                           )
