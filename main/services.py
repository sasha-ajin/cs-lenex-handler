import xml.etree.ElementTree as et
from .models import Athlete, Meet, Club, Record, Enrollment
from .classes_schemas import RecordSchema, ClubSchema, AthleteSchema, MeetSchema, EnrollmentSchema
from marshmallow import ValidationError


def file_xml_handle(file_xml):
    root = (et.parse(file_xml)).getroot()
    error_result = {'meets_quantity': 0, 'clubs_quantity': 0, 'athletes_quantity': 0, 'errors': True, 'error_msg': ''}
    meet_tag = root.find('MEETS/MEET')
    clubs, athletes, enrollment_record = list(), list(), dict()
    data_meet = dict(
        name=meet_tag.attrib['name'], city=meet_tag.attrib['city'], deadline=meet_tag.attrib['deadline'],
        entrystartdate=meet_tag.attrib['entrystartdate'], entrytype=meet_tag.attrib['entrytype'],
        reservecount=meet_tag.attrib['reservecount'], startmethod=meet_tag.attrib['startmethod'],
        timing=meet_tag.attrib['timing'], nation=meet_tag.attrib['nation']
    )
    for club_tag in root.iter('CLUB'):
        club_attr = club_tag.attrib
        data_club = {
            'code': club_attr['code'], 'nation': club_attr['nation'], 'clubid': club_attr['clubid'],
            'name': club_attr['name'], 'type': club_attr['type']
        }
        athlete_tags = club_tag.findall(f"./ATHLETES/ATHLETE")
        for athlete_tag in athlete_tags:
            data_athlete = {
                'birthdate': athlete_tag.attrib['birthdate'], 'firstname': athlete_tag.attrib['firstname'],
                'lastname': athlete_tag.attrib['lastname'], 'gender': athlete_tag.attrib['gender'],
                'nation': athlete_tag.attrib['nation'], 'athleteid': athlete_tag.attrib['athleteid']
            }
            data_enrollment = {'athlete': data_athlete, 'club': data_club, 'meet': data_meet}
            result_tags = athlete_tag.findall(f"./RESULTS/RESULT")
            enrollment_id = str(data_athlete['athleteid']) + str(data_club['clubid'])
            enrollment_record[enrollment_id] = {'records': []}
            for result_tag in result_tags:
                result_attr = result_tag.attrib
                event_tag = (meet_tag.find(
                    f".//EVENT/AGEGROUPS/AGEGROUP/RANKINGS/RANKING[@resultid='{result_attr['resultid']}']........"))
                ranking_attr = (event_tag.find(f".//RANKING[@resultid='{result_attr['resultid']}']")).attrib
                agegroup_attr = (event_tag.find(f".//RANKING[@resultid='{result_attr['resultid']}']....")).attrib
                swimstyle_attr = (event_tag.find(f"./SWIMSTYLE")).attrib
                event_attr = event_tag.attrib
                try:
                    enrollment_record[enrollment_id]['records'].append(RecordSchema().load(data={
                        'enrollment': data_enrollment, 'order': ranking_attr['order'], 'place': ranking_attr['place'],
                        'resultid': result_attr['resultid'], 'agemin': agegroup_attr['agemin'],
                        'agemax': agegroup_attr['agemax'], 'distance': swimstyle_attr['distance'],
                        'stroke': swimstyle_attr['stroke'], 'event_gender': event_attr['gender'],
                        'event_number': event_attr['number'], 'event_order': event_attr['order']
                    }))
                except ValidationError as er:
                    error_result['error_msg'] = er.messages
                    return error_result
            enrollment_record[enrollment_id]['obj'] = EnrollmentSchema().load(data=data_enrollment)
            athletes.append(AthleteSchema().load(data=data_athlete))
        clubs.append(ClubSchema().load(data=data_club))
    results = data_adding(athletes, clubs, enrollment_record, MeetSchema().load(data=data_meet))
    if (
            results['club_created'] > 0 or results['athlete_created'] > 0 or
            results['record_created'] > 0 or results['enrollment_created'] > 0
    ):
        results['created'] = True
    else:
        results['created'] = False
    if results['club_updated'] > 0 or results['athlete_updated'] > 0 or results['record_updated'] > 0:
        results['updated'] = True
    else:
        results['updated'] = False
    return results


def data_adding(athlete_objs, club_objs, enrollment_records_objs, meet_obj):
    athletes, athletes_extra, clubs, clubs_extra, records, records_extra, enrollments = [], [], [], [], [], [], []
    athletes_db, clubs_db = {}, {}  # lists with objects from database
    club_created, athlete_created, record_created, enrollment_created, meet_created = 0, 0, 0, 0, 0  # counters of created objects
    club_updated, athlete_updated, record_updated, meet_updated = 0, 0, 0, 0  # counters of updated objects
    # Meet creating or updating:
    meets_quantity = Meet.objects.filter(name=meet_obj.name, entrystartdate=meet_obj.entrystartdate).count()
    if meets_quantity < 1:
        meet_db = Meet.objects.create(city=meet_obj.city, name=meet_obj.name, course=meet_obj.course,
                                      deadline=meet_obj.deadline, entrystartdate=meet_obj.entrystartdate,
                                      entrytype=meet_obj.entrytype, nation=meet_obj.nation
                                      , reservecount=meet_obj.reservecount, startmethod=meet_obj.startmethod,
                                      timing=meet_obj.timing)
        meet_created = 1
    else:
        meet_db = Meet.objects.get(name=meet_obj.name, entrystartdate=meet_obj.entrystartdate)
        data_meet_new = {'city': meet_obj.city, 'course': meet_obj.course, 'deadline': meet_obj.deadline,
                         'entrystartdate': meet_obj.entrystartdate, 'entrytype': meet_obj.entrytype,
                         'reservecount': meet_obj.reservecount, 'startmethod': meet_obj.startmethod,
                         'timing': meet_obj.timing, 'nation': meet_obj.nation}
        data_meet_old = {'city': meet_db.city, 'course': meet_db.course, 'deadline': meet_db.deadline,
                         'entrystartdate': meet_db.entrystartdate, 'entrytype': meet_db.entrytype,
                         'reservecount': meet_db.reservecount, 'startmethod': meet_db.startmethod,
                         'timing': meet_db.timing, 'nation': meet_db.nation}
        if data_meet_new != data_meet_old:
            Meet.objects.filter(pk=meet_db.pk).update(**data_meet_new)
            meet_updated = 1

    # Creating lists with objects from database:
    for athlete in Athlete.objects.all():
        athletes.append({'firstname': athlete.firstname, 'lastname': athlete.lastname, 'birthdate': athlete.birthdate})
        athletes_extra.append({'nation': athlete.nation, 'gender': athlete.gender})  # extra fields which can be changed
        athletes_db[athlete.firstname + athlete.lastname + str(athlete.birthdate)] = athlete
    for club in Club.objects.all():
        clubs.append({'name': club.name, 'nation': club.nation})
        clubs_extra.append({'code': club.code, 'type': club.type})  # extra fields which can be changed
        clubs_db[club.name + club.nation] = club
    for enrollment in Enrollment.objects.filter(meet__name=meet_obj.name, meet__entrystartdate=meet_obj.entrystartdate):
        enrollments.append({'athlete': {'firstname': enrollment.athlete.firstname,
                                        'lastname': enrollment.athlete.lastname,
                                        'birthdate': enrollment.athlete.birthdate},
                            'club': {'name': enrollment.club.name, 'nation': enrollment.club.nation}})
    for record in Record.objects.filter(enrollment__meet__name=meet_obj.name,
                                        enrollment__meet__entrystartdate=meet_obj.entrystartdate):
        records.append({'enrollment': {
            'athlete': {'firstname': record.enrollment.athlete.firstname, 'lastname': record.enrollment.athlete.lastname
                , 'birthdate': record.enrollment.athlete.birthdate},
            'club': {'name': record.enrollment.club.name, 'nation': record.enrollment.club.nation}
        },
            'stroke': record.stroke, 'agemin': record.agemin, 'agemax': record.agemax, 'distance': record.distance
        })
        records_extra.append({'order': record.order, 'place': record.place,
                              'event_gender': record.event_gender, 'event_number': record.event_number,
                              'event_order': record.event_order})  # extra fields which can be changed

    # Creating or updating objects in database:
    for athlete in athlete_objs:
        data_athlete = [{'firstname': athlete.firstname, 'lastname': athlete.lastname, 'birthdate': athlete.birthdate},
                        {'nation': athlete.nation, 'gender': athlete.gender}]
        if data_athlete[0] in athletes:  # Checking if we have this athlete in database
            if data_athlete[1] != athletes_extra[athletes.index(data_athlete[0])]:  # Check if some  field was changed
                ath_db = Athlete.objects.get(firstname=athlete.firstname, lastname=athlete.lastname,
                                             birthdate=athlete.birthdate)
                ath_db.nation, ath_db.gender = athlete.nation, athlete.gender
                ath_db.save()
                athletes_db[athlete.athleteid] = ath_db
                athlete_updated += 1
        else:
            ath_db = Athlete.objects.create(firstname=athlete.firstname, lastname=athlete.lastname,
                                            birthdate=athlete.birthdate, nation=athlete.nation, gender=athlete.gender)
            athletes_db[athlete.athleteid] = ath_db
            athlete_created += 1
    for club in club_objs:
        data_club = [{'name': club.name, 'nation': club.nation}, {'code': club.code, 'type': club.type}]
        if data_club[0] in clubs:  # Checking if we have this club in database
            if data_club[1] != clubs_extra[clubs.index(data_club[0])]:  # checking if some extra fields were changed
                club_db = Club.objects.get(name=club.name, nation=club.nation)
                club_db.code, club_db.type = club.code, club.type
                club_db.save()
                clubs_db[club.clubid] = club_db
                club_updated += 1
        else:
            club_db = Club.objects.create(code=club.code, nation=club.nation, name=club.name, type=club.type)
            clubs_db[club.clubid] = club_db
            club_created += 1
    for enrollment in enrollment_records_objs.values():
        data_enrollment = {'athlete': {'firstname': enrollment['obj'].athlete.firstname,
                                       'lastname': enrollment['obj'].athlete.lastname,
                                       'birthdate': enrollment['obj'].athlete.birthdate},
                           'club': {'name': enrollment['obj'].club.name, 'nation': enrollment['obj'].club.nation}}
        if data_enrollment not in enrollments:  # Checking if we have this enrollment in database
            athlete, club = enrollment['obj'].athlete, enrollment['obj'].club
            athlete_id = str(athlete.firstname) + str(athlete.lastname) + str(athlete.birthdate)
            club_id = str(club.name) + str(club.nation)
            if athlete_id in athletes_db:
                athlete_db = athletes_db[athlete_id]
            else:
                athlete_db = Athlete.objects.get(firstname=athlete.firstname, lastname=athlete.lastname,
                                                 birthdate=athlete.birthdate)
                athletes_db[athlete_id] = athlete_db
            if club_id in clubs_db:
                club_db = clubs_db[club_id]
            else:
                club_db = Club.objects.get(name=enrollment['obj'].club.name, nation=enrollment['obj'].club.nation)
                clubs_db[club_id] = club_db
            enrollment_db = Enrollment.objects.create(athlete=athlete_db, club=club_db, meet=meet_db)
            enrollment_created += 1
        else:
            data_athlete, data_club = data_enrollment['athlete'], data_enrollment['club']
            enrollment_db = Enrollment.objects.get(meet=meet_db, athlete__firstname=data_athlete['firstname'],
                                                   athlete__lastname=data_athlete['lastname'],
                                                   athlete__birthdate=data_athlete['birthdate'],
                                                   club__name=data_club['name'], club__nation=data_club['nation'])
        for record in enrollment['records']:
            data_record = [{
                'enrollment': {
                    'athlete': {'firstname': record.enrollment.athlete.firstname,
                                'lastname': record.enrollment.athlete.lastname,
                                'birthdate': record.enrollment.athlete.birthdate},
                    'club': {'name': record.enrollment.club.name, 'nation': record.enrollment.club.nation}
                },
                'stroke': record.stroke, 'agemin': record.agemin, 'agemax': record.agemax, 'distance': record.distance
            },
                {'order': record.order, 'place': record.place, 'event_gender': record.event_gender,
                 'event_number': record.event_number, 'event_order': record.event_order}]
            if data_record[0] in records:  # Checking if we have this record in database
                if data_record[1] != records_extra[records.index(data_record[0])]:  # check if extra fields were changed
                    record_db = Record.objects.get(enrollment=enrollment_db, stroke=record.stroke, agemax=record.agemax,
                                                   agemin=record.agemin, distance=record.distance)
                    record_db.order, record_db.place, record_db.event_gender, record_db.event_number, \
                    record_db.event_order = record.order, record.place, record.event_gender, record.event_number, record.event_order
                    record_db.save()
                    record_updated += 1
            else:
                Record.objects.create(
                    enrollment=enrollment_db, order=record.order, place=record.place, agemin=record.agemin,
                    agemax=record.agemax, distance=record.distance, stroke=record.stroke,
                    event_order=record.event_order,
                    event_gender=record.event_gender, event_number=record.event_number,
                )
                record_created += 1
    result = {'club_created': club_created, 'athlete_created': athlete_created, 'record_created': record_created,
              'enrollment_created': enrollment_created, 'club_updated': club_updated, 'meet_created': meet_created,
              'athlete_updated': athlete_updated, 'record_updated': record_updated, 'meet_updated': meet_updated,
              'errors': False}
    return result


def error_reader(errors_dict):
    for error in errors_dict:
        if type(errors_dict[error]) is dict:
            return error_reader(errors_dict=errors_dict[error])
        else:
            return [error, errors_dict[error]]
