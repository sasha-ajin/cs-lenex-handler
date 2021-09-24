from marshmallow import Schema, fields, validate, post_load
from docs.nations_list import nations


class AthleteClass:
    def __init__(self, birthdate, firstname, lastname, gender, nation, athleteid):
        self.birthdate = birthdate
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.nation = nation
        self.athleteid = athleteid


class ClubClass:
    def __init__(self, code, nation, clubid, name, type):
        self.code = code
        self.nation = nation
        self.clubid = clubid
        self.name = name
        self.type = type

    def __repr__(self):
        return f"{self.name}"


class AthleteClubClass:
    def __init__(self, athlete, club):
        self.athlete = athlete
        self.club = club

    def __repr__(self):
        return f"{self.athlete.firstname}/{self.club.name}"


class MeetClass:
    def __init__(self, city, name, course, deadline, entrystartdate, entrytype, reservecount,
                 startmethod, timing, nation, athleteclubs=[], clubs=[]):
        self.clubs = clubs
        self.athleteclubs = athleteclubs
        self.city = city
        self.name = name
        self.course = course
        self.deadline = deadline
        self.entrystartdate = entrystartdate
        self.entrytype = entrytype
        self.reservecount = reservecount
        self.startmethod = startmethod
        self.timing = timing
        self.nation = nation

    def __repr__(self):
        return f"{self.athleteclubs} " \
               f"{self.clubs}"


class AthleteSchema(Schema):
    gender = fields.String(validate=validate.OneOf(['M', 'F']))
    birthdate = fields.Date('%Y-%m-%d')
    firstname = fields.String()
    lastname = fields.String()
    nation = fields.String(validate=validate.OneOf(nations))
    athleteid = fields.String()

    @post_load
    def make_obj(self, data, **kwargs):  # название метода может быть любым
        return AthleteClass(**data)


class ClubSchema(Schema):
    type = fields.String(validate=validate.OneOf(['CLUB', 'NATIONALTEAM', 'REGIONALTEAM', 'UNATTACHED']), required=True)
    code = fields.String(required=True)
    nation = fields.String(validate=validate.OneOf(nations), required=True)
    name = fields.String(required=True)
    clubid = fields.String(required=True)

    @post_load
    def make_obj(self, data, **kwargs):  # название метода может быть любым
        return ClubClass(**data)


class AthleteClubSchema(Schema):
    athlete = fields.Nested(AthleteSchema(), many=False, )
    club = fields.Nested(ClubSchema(), many=False)

    @post_load
    def make_obj(self, data, **kwargs):  # название метода может быть любым
        return AthleteClubClass(**data)


class MeetSchema(Schema):
    clubs = fields.List(fields.Nested(ClubSchema()), required=False)
    athleteclubs = fields.List(fields.Nested(AthleteClubSchema()), required=False)
    city = fields.String(required=True)
    name = fields.String(required=True)
    course = fields.String(validate=validate.OneOf(
        ['LCM', 'SCM', 'SCY', 'SCM16', 'SCM20', 'SCM33', 'SCY20', 'SCY27', 'SCY33', 'SCY36', 'OPEN']))
    deadline = fields.Date('%Y-%m-%d')
    entrystartdate = fields.Date('%Y-%m-%d', required=True)
    entrytype = fields.String(validate=validate.OneOf(['OPEN', 'INVITATION']), required=True)
    reservecount = fields.Integer(required=True)
    startmethod = fields.String(validate=validate.OneOf(['1', '2']))
    timing = fields.String(validate=validate.OneOf(['AUTOMATIC', 'MANUAL3', 'MANUAL1']))
    nation = fields.String(validate=validate.OneOf(nations))

    @post_load
    def make_obj(self, data, **kwargs):
        return MeetClass(**data)


def cc():
    data_club = {
        'type': 'CLUB',
        'code': 'VIH',
        'nation': 'BUL',
        'clubid': '1316',
        'name': 'Vihren'
    }
    data_athlete = {
        'birthdate': '2005-12-30',
        'firstname': 'Kristiyan',
        'gender': 'M',
        'lastname': 'Spiriev',
        'nation': 'BUL',
        'athleteid': '1350'
    }
    data_athlete_club = {
        'athlete': data_athlete,
        'club': data_club
    }
    sch = AthleteClubSchema()
    ac_res = sch.load(data_athlete_club)
    print(ac_res.club)
    data_meet = {
        'clubs': [],
        'athleteclubs': [data_athlete_club, data_athlete_club],
        'city': 'Plovdiv',
        'name': '1',
        'course': 'SCM',
        'deadline': '2021-03-15',
        'entrystartdate': '2021-03-07',
        'entrytype': 'OPEN',
        'reservecount': '1',
        'startmethod': '1',
        'timing': 'AUTOMATIC',
        'nation': 'BUL'
    }
    sch = MeetSchema()
    meet_res = sch.load(data=data_meet)