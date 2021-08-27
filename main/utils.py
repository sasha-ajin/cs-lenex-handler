import xml.etree.ElementTree as et


def file_txt_handle(file_txt):
    with open(file_txt, "r") as file:
        list_countries = list()
        for line in file:
            line = (line.split('\n')[0]).split('=')
            list_countries.append(tuple(line))
        choice = tuple(list_countries)
        return choice


def file_xml_handle(file_xml):
    root = (et.parse(file_xml)).getroot()
    meets_list = list()
    for child in root:
        if child.tag == 'MEETS':
            for meet in child:
                meet.attrib['clubs'] = list()
                meets_list.append(meet.attrib)
                for child_meet in meet:
                    if child_meet.tag == 'CLUBS':
                        for club in child_meet:
                            club.attrib['athletes'] = list()
                            meets_list[len(meets_list) - 1]['clubs'].append(dict(club.attrib))
                            for child_club in club:
                                if child_club.tag == 'ATHLETES':
                                    for athlete in child_club:
                                        club_list_len = len(meets_list[len(meets_list) - 1]['clubs'])
                                        meets_list[len(meets_list) - 1]['clubs'][club_list_len - 1]['athletes'].append(
                                            athlete.attrib)
    return meets_list