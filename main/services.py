import xml.etree.ElementTree as et
from .models import Athlete, Meet, Club, AthleteClub
from .classes_schemas import MeetSchema, ClubSchema, AthleteClubSchema
from pprint import pprint


def file_xml_handle(file_xml):
    root = (et.parse(file_xml)).getroot()
    meets_list = list()
    for child in root:
        if child.tag == 'MEETS':
            for meet in child:
                data_meet = dict(name=meet.attrib['name'], city=meet.attrib['city'], course=meet.attrib['course'],
                                 deadline=meet.attrib['deadline'],
                                 entrystartdate=meet.attrib['entrystartdate'], entrytype=meet.attrib['entrytype'],
                                 reservecount=meet.attrib['reservecount'], startmethod=meet.attrib['startmethod'],
                                 timing=meet.attrib['timing'], nation=meet.attrib['nation'], clubs=[], athleteclubs=[])
                try:
                    meet_obj = MeetSchema().load(data=data_meet)
                except Exception:
                    print('meet error')
                    return {'meets_quantity': int(), 'clubs_quantity': int(), 'athletes_quantity': int(),
                            'errors': True}
                print(meet_obj.clubs)
                meets_list.append(meet_obj)
                for child_meet in meet:
                    if child_meet.tag == 'CLUBS':
                        for club in child_meet:
                            data_club = {'code': club.attrib['code'],
                                         'nation': club.attrib['nation'],
                                         'clubid': club.attrib['clubid'], 'name': club.attrib['name'],
                                         'type': club.attrib['type']}
                            try:
                                club_obj = ClubSchema().load(data=data_club)
                                meet_obj.clubs.append(club_obj)
                            except Exception:
                                print('club error')
                                return {'meets_quantity': int(), 'clubs_quantity': int(), 'athletes_quantity': int(),
                                        'errors': True}
                            for child_club in club:
                                if child_club.tag == 'ATHLETES':
                                    for athlete in child_club:
                                        data_athlete = {'birthdate': athlete.attrib['birthdate'],
                                                        'firstname': athlete.attrib['firstname'],
                                                        'lastname': athlete.attrib['lastname'],
                                                        'gender': athlete.attrib['gender'],
                                                        'nation': athlete.attrib['nation'],
                                                        'athleteid': athlete.attrib['athleteid']}
                                        try:
                                            athlete_club_obj = AthleteClubSchema().load(
                                                {'athlete': data_athlete, 'club': data_club})
                                            meet_obj.athleteclubs.append(athlete_club_obj)
                                        except Exception:
                                            print('ath error')
                                            return {'meets_quantity': int(), 'clubs_quantity': int(),
                                                    'athletes_quantity': int(), 'errors': True}
    result = data_adding(meet_obj)
    return {'meets_quantity': result['meets_quantity'], 'clubs_quantity': result['clubs_quantity'],
            'athletes_quantity': result['athletes_quantity'], 'errors': False}


def data_adding(meet_obj):
    meets_quantity, clubs_quantity, athletes_quantity = 1, int(), int()
    meet_db = Meet.objects.create(city=meet_obj.city, name=meet_obj.name, course=meet_obj.course,
                                  deadline=meet_obj.deadline, entrystartdate=meet_obj.entrystartdate,
                                  entrytype=meet_obj.entrytype, reservecount=meet_obj.reservecount,
                                  startmethod=meet_obj.startmethod, timing=meet_obj.timing,
                                  nation=meet_obj.nation)
    club_ids_qs = Club.objects.all().values_list('clubid', flat=True)
    athlete_ids_qs = Athlete.objects.values_list('athleteid', flat=True)
    club_ids = list()
    athlete_ids = list()
    for cl_id in club_ids_qs:
        club_ids.append(cl_id)
    for ath_id in athlete_ids_qs:
        athlete_ids.append(ath_id)
    for club in meet_obj.clubs:
        if club.clubid in club_ids:
            meet_db.clubs.add(Club.objects.get(clubid=club.clubid))
        else:
            meet_db.clubs.add(
                Club.objects.create(code=club.code, nation=club.nation, clubid=club.clubid, name=club.name,
                                    type=club.type))
            club_ids.append(club.clubid)
            clubs_quantity += 1
    for ath_club in meet_obj.athleteclubs:
        if ath_club.athlete.athleteid in athlete_ids:
            current_athlete = Athlete.objects.get(athleteid=ath_club.athlete.athleteid)
            current_club = Club.objects.get(clubid=ath_club.club.clubid)
            try:
                meet_db.athleteclubs.add(AthleteClub.objects.get(athlete=current_athlete, club=current_club))
            except:
                meet_db.athleteclubs.add(AthleteClub.objects.create(athlete=current_athlete, club=current_club))
        else:
            Athlete.objects.create(birthdate=ath_club.athlete.birthdate, firstname=ath_club.athlete.firstname,
                                   lastname=ath_club.athlete.lastname, gender=ath_club.athlete.gender,
                                   nation=ath_club.athlete.gender, athleteid=ath_club.athlete.athleteid)
            meet_db.athleteclubs.add(
                AthleteClub.objects.create(athlete=Athlete.objects.get(athleteid=ath_club.athlete.athleteid),
                                           club=Club.objects.get(clubid=ath_club.club.clubid)))
            athletes_quantity += 1
            athlete_ids.append(ath_club.athlete.athleteid)
    return {'meets_quantity': meets_quantity, 'clubs_quantity': clubs_quantity, 'athletes_quantity': athletes_quantity}
