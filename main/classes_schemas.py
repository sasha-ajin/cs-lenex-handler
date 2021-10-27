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

    def __repr__(self):
        return f"{self.firstname} {self.lastname}"


class ClubClass:
    def __init__(self, nation, clubid, name, type, code=''):
        self.code = code
        self.nation = nation
        self.clubid = clubid
        self.name = name
        self.type = type

    def __repr__(self):
        return f"{self.name}"


class MeetClass:
    def __init__(self, city, name, deadline, entrystartdate, entrytype,
                 startmethod, timing, nation, reservecount=0, course=''):
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
        return self.name


class Enrollment:
    def __init__(self, athlete, club, meet):
        self.athlete = athlete
        self.club = club
        self.meet = meet

    def __repr__(self):
        return f"{self.athlete.firstname}|{self.club.name}"


class Record:
    def __init__(self, enrollment, order, place, resultid, agemin, agemax, distance, stroke, event_gender,
                 event_number, event_order):
        self.enrollment = enrollment
        self.order = order
        self.place = place
        self.resultid = resultid
        self.agemin = agemin
        self.agemax = agemax
        self.distance = distance
        self.stroke = stroke
        self.event_gender = event_gender
        self.event_number = event_number
        self.event_order = event_order

    def __repr__(self):
        return f"{self.enrollment.athlete.firstname}/{self.place}/{self.event_gender}"


class AthleteSchema(Schema):
    birthdate = fields.Date('%Y-%m-%d', required=True)
    firstname = fields.String(required=True, validate=validate.Length(max=50))
    lastname = fields.String(required=True, validate=validate.Length(max=50))
    gender = fields.String(validate=validate.OneOf(['M', 'F', 'Male', 'Female']), required=True)
    nation = fields.String(validate=validate.OneOf(nations), required=True)
    athleteid = fields.String(required=True, validate=validate.Length(max=100))

    @post_load
    def make_obj(self, data, **kwargs):
        return AthleteClass(**data)


class ClubSchema(Schema):
    code = fields.String(validate=validate.Length(max=20), required=False)
    nation = fields.String(validate=validate.OneOf(nations), required=True)
    clubid = fields.String(required=True, validate=validate.Length(max=100))
    name = fields.String(required=True, validate=validate.Length(max=50))
    type = fields.String(validate=validate.OneOf(['CLUB', 'NATIONALTEAM', 'REGIONALTEAM', 'UNATTACHED']), required=True,
                         default='UNATTACHED')

    @post_load
    def make_obj(self, data, **kwargs):
        return ClubClass(**data)


class MeetSchema(Schema):
    city = fields.String(required=True, validate=validate.Length(max=50))
    name = fields.String(required=True, validate=validate.Length(max=50))
    course = fields.String(required=False, validate=validate.OneOf(
        ['LCM', 'SCM', 'SCY', 'SCM16', 'SCM20', 'SCM33', 'SCY20', 'SCY27', 'SCY33', 'SCY36', 'OPEN']))
    deadline = fields.Date('%Y-%m-%d')
    entrystartdate = fields.Date('%Y-%m-%d', required=True)
    entrytype = fields.String(validate=validate.OneOf(['OPEN', 'INVITATION']), required=True)
    reservecount = fields.Integer(required=False, default=0)
    startmethod = fields.String(validate=validate.OneOf(['1', '2']))
    timing = fields.String(validate=validate.OneOf(['AUTOMATIC', 'MANUAL3', 'MANUAL1']))
    nation = fields.String(validate=validate.OneOf(nations), required=True)

    @post_load
    def make_obj(self, data, **kwargs):
        return MeetClass(**data)


class EnrollmentSchema(Schema):
    athlete = fields.Nested(AthleteSchema(), many=False)
    club = fields.Nested(ClubSchema(), many=False)
    meet = fields.Nested(MeetSchema(), many=False)

    @post_load
    def make_obj(self, data, **kwargs):
        return Enrollment(**data)


class RecordSchema(Schema):
    enrollment = fields.Nested(EnrollmentSchema(), many=False)
    order = fields.Integer(required=True)
    place = fields.Integer(required=True)
    resultid = fields.String(required=True, validate=validate.Length(max=30))
    agemin = fields.Integer(required=True)
    agemax = fields.Integer(required=True)
    distance = fields.Integer(required=True)
    stroke = fields.String(validate=validate.OneOf(
        ['APNEA', 'BACK', 'BIFINS', 'BREAST', 'FLY', 'FREE', 'IMMERSION', 'MEDLEY', 'SURFACE', 'UNKNOWN']
    ))
    event_gender = fields.String(validate=validate.OneOf(['M', 'F', 'Male', 'Female']))
    event_number = fields.Integer()
    event_order = fields.Integer()

    @post_load
    def make_obj(self, data, **kwargs):
        return Record(**data)