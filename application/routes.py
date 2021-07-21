from . import app, db
from .models import Player, Team
from .forms import TeamForm, PlayerForm
from flask import redirect, url_for, request, render_template

@app.route("/")
def home():
    teams = Team.query.all()
    players = Player.query.all()

    return render_template("home.html", teams=teams, players=players)

@app.route("/create", methods=["GET", "POST"])
def create():
    form = TeamForm()

    if request.method == "POST":
        new_team = Team(
            description=form.description.data,
            )
        db.session.add(new_team)
        db.session.commit()

        return redirect(url_for("home"))
    else:

        return render_template("create_task.html", form=form)

@app.route("/create_label", methods=["GET", "POST"])
def create_label():
    form1 = TeamForm()
    form2 = PlayerForm()

    teams = Team.query.all()
    form2.team.choices = [(team.id, team.description) for team in teams]

    if request.method == "POST":
        new_player = Player(name=form2.name.data, position=form2.position.data, team_id=form2.team.data)
        db.session.add(new_player)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return render_template("create_label.html", form=form2)

@app.route("/update/<int:id>/", methods=["GET", "POST"])
def update(id):
    team = Team.query.get(id)
    form1 = TeamForm()
    form2 = PlayerForm()

    if request.method == "POST":
        team.description = form1.description.data
        team.players.id = form2.name.data
        db.session.add(team)
        db.session.commit()

        return redirect(url_for("home"))
    else:
        players = Player.query.all()
        form2.name.choices = [(player.id, player.team) for player in players]

        form1.description.data = team.description

        return render_template("create_task.html", form=form1)

@app.route("/update_player/<int:id>", methods=["GET", "POST"])
def update_player(id):
    player = Player.query.get(id)
    form1 = TeamForm()
    form2 = PlayerForm()

    teams = Team.query.all()
    form2.team.choices = [(team.id, team.description) for team in teams]

    if request.method == "POST":
        player.name = form2.name.data
        player.position = form2.position.data
        player.team_id = form2.team.data
        db.session.add(player)
        db.session.commit()

        return redirect(url_for("home"))
    else:
        players = Player.query.all()
        form2.name.choices = [(player.id, player.team) for player in players]

        form2.name.data = player.name
        form2.position.data = player.position
        form2.team.data = player.team_id

        return render_template("create_label.html", form=form2)

@app.route("/delete/<int:id>")
def delete(id):
    team = Team.query.get(id)
    db.session.delete(team)
    db.session.commit()

    return redirect(url_for("home"))

@app.route("/complete/<int:id>")
def complete(id):
    player = Player.query.get(id)
    player.active = True
    db.session.add(player)
    db.session.commit()

    return redirect(url_for("home"))

@app.route("/incomplete/<int:id>")
def incomplete(id):
    player = Player.query.get(id)
    player.active = False
    db.session.add(player)
    db.session.commit()

    return redirect(url_for("home"))

    