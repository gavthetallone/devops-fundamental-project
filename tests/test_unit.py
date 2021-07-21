from flask import url_for
from flask_testing import TestCase
from application import app, db
from application.models import Team, Player, League

class TestBase(TestCase):
    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI="sqlite:///test.db",
            DEBUG=True,
            WTF_CSRF_ENABLED=False
        )
        return app

    def setUp(self):
        db.create_all()

        db.session.add(League(name="Run unit tests"))
        db.session.add(League(name="Do something else"))
        db.session.add(Player(name="Random", position="QB", active=True))

        db.session.commit()

    def tearDown(self):
        db.drop_all()

class TestViews(TestBase):
    def test_home(self):
        response = self.client.get(url_for("home"))
        self.assert200(response)
    
    def test_create(self):
        response = self.client.get(url_for("create_league"))
        self.assert200(response)
    
    def test_update(self):
        response = self.client.get(url_for("update_league", id=1))
        self.assert200(response)


class TestRead(TestBase):
    def test_home(self):
        response = self.client.get(url_for("home"))
        assert "Run unit tests" in response.data.decode()
        assert "Do something else" in response.data.decode()

class TestCreate(TestBase):
    def test_create_league(self):
        response = self.client.post(
            url_for("create_league"),
            data={"name" : "Check create is working"},
            follow_redirects=True
            )
        
        assert "Check create is working" in response.data.decode()

    def test_create_team(self):
        response = self.client.post(
            url_for("create_team"),
            data={"description" : "Example team",
            "league_id" : 1},
            follow_redirects=True
            )
        
        assert Team.query.filter_by(description="Example team").first() != None
    
    
    def test_create_player(self):
        response = self.client.post(
            url_for("create_player"),
            data={"name" : "Example player",
            "position" : "QB",
            "team_id" : 1},
            follow_redirects=True
            )
        
        assert Player.query.filter_by(name="Example player").first() != None

class TestUpdate(TestBase):
    def test_update(self):
        response = self.client.post(
            url_for("update_league", id=1),
            data={"name" : "Check update is working"},
            follow_redirects=True
            )
        
        assert "Check update is working" in response.data.decode()
        assert "Do something else" in response.data.decode()
        assert "Run unit tests" not in response.data.decode()

    # def test_inactive(self):
    #     response = self.client.get(
    #         url_for("inactive", id=1),
    #         follow_redirects=True
    #         )
    #     print(response.data.decode())
    #     assert "❌" in response.data.decode()
    
    # def test_active(self):
    #     response = self.client.get(
    #         url_for("active", id=1),
    #         follow_redirects=True
    #         )
    #     print(response.data.decode())
    #     assert "✔️" in response.data.decode()

class TestDelete(TestBase):
    def test_delete(self):
        response = self.client.get(
            url_for("delete_league", id=1),
            follow_redirects=True
            )

        assert "Do something else" in response.data.decode()
        assert "Run unit tests" not in response.data.decode()
        