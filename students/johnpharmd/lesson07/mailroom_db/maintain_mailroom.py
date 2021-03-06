import sys
from peewee import SqliteDatabase
from peewee import Model
from peewee import CharField
from peewee import IntegerField


database = SqliteDatabase('mailroom.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    class Meta:
        database = database


class Donor(BaseModel):
    """
        This class defines Donor instances, each of which maintains
        details of an individual donor.
    """
    title = CharField(max_length=10)
    last_name = CharField(primary_key=True, max_length=30)
    total_donation_amt = IntegerField()
    num_donations = IntegerField()


def get_donor_list():
    print([donor.last_name for donor in Donor])


def query_donor_info():
    title = input('Enter donor title: ')
    last_name = input('Enter last name: ')
    total_donation_amt = int(input('Enter total donation amount: '))
    num_donations = int(input('Enter number of donations: '))
    query_dict = {'title': title, 'last_name': last_name,
                  'total_donation_amt': total_donation_amt,
                  'num_donations': num_donations}
    return query_dict


def add_donor(**kwargs):
    if kwargs:
        updated_donor = Donor.create(**kwargs)
        print(updated_donor.title, updated_donor.last_name, 'updated')
        updated_donor.save()
    else:
        q_title = input('Enter donor title: ')
        q_lastname = input('Enter last name: ')
        q_donation = int(input('Donation amount (USD)?: '))
        new_donor = Donor.create(
                                 title=q_title,
                                 last_name=q_lastname,
                                 total_donation_amt=q_donation,
                                 num_donations=1
                                 )
        new_donor.save()
        print(q_title, q_lastname, 'added to database')


def update_or_remove_donor():
    q_title = input('Enter donor title: ')
    q_lastname = input('Enter last name: ')
    response = input('[U]pdate or [r]emove this donor? ')
    for donor in (Donor.select()
                       .where((Donor.title == q_title) &
                              (Donor.last_name == q_lastname))):
        print(donor.title, donor.last_name, donor.total_donation_amt,
              donor.num_donations)
        donor.delete_instance()
        if response.lower() == 'u':
            print('Re-enter values for each of the donor\'s fields')
            add_donor(**query_donor_info())
        elif response.lower() == 'r':
            print('Donor removed from database')


def get_report():
    print()
    psv = ['Donor Name', '| Total Given', '| Num Gifts',
           '| Average Gift']
    print('{:<15}{:>12}{:>12}{:>12}'.format(psv[0], psv[1],
          psv[2], psv[3]))
    for i in range(55):
        print('-', end='')
    print()
    new_list = []
    for donor in Donor:
        new_list.append([donor.total_donation_amt, donor.last_name,
                        donor.num_donations])
    new_list.sort(reverse=True)
    for donor_list in new_list:
        formatted_donor = ('{:<15}'.format(donor_list[1])
                           + '{}{:>10}'.format(' $', donor_list[0])
                           + '{:>13}'.format(donor_list[2])
                           + '{}{:>11}'.format(' $',
                           donor_list[0] // donor_list[2]))
        print(formatted_donor)


class UI():
    def __init__(self):
        database.create_tables([Donor])
        donors = Donor.select()
        menu_dct = {'1': get_donor_list,
                    '2': get_report,
                    '3': add_donor,
                    '4': update_or_remove_donor,
                    'q': sys.exit}
        main_text = '\n'.join((
                               'Choose from the following:',
                               '"1" - Get a List of Donors,',
                               '"2" - Create a Report,',
                               '"3" - Add a Donor,',
                               '"4" - Update or Remove a Donor, or',
                               '"q" to Quit: '
                               ))
        while True:
            print('\nMain Menu:')
            response = input(main_text)
            print()
            try:
                if response == 'q':
                    database.close()
                    print('Program execution completed.')
                menu_dct[response]()

            except KeyError:
                print('\nThat selection is invalid. Please try again.')


interaction_instance = UI()
