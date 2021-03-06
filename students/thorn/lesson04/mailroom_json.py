"""
Thomas Horn

Mailroom refactor to use JSON to load and save
"""

import os
import json
import json_save.json_save.json_save_dec as jsd


@jsd.json_save
class Donor:
    """
    Information about single donors.
    """

    # Saveables objects setup
    name = jsd.String()
    donations = jsd.List()
    
    def __init__(self, name, donations=None):
        self.name = name
        self.donations = donations

    @property
    def donor_totals(self):
        # Takes in a list --> use sum this time
        return sum(self.donations)

    @property
    def num_donations(self):
        return len(self.donations)

    @property
    def average_donations(self):
        return self.donor_totals / self.num_donations

    def add_donation(self, donation):
        self.donations.append(donation)

    """
    OO Sorting.
    """
    def __lt__(self, other):
        return self.donor_totals < other.donor_totals

    def __gt__(self, other):
        return self.donor_totals > other.donor_totals


@jsd.json_save
class DonorList:
    """
    Holds a list of donor objects.

    Performs following after user inputs a donor:
        'list' input --> shows a list of donor names and reprompts
        adds donor if they do not exist or uses existing user
        prompts for a donation amd adds to donor
        prints thank you note
    """

    donors = jsd.List()

    def __init__(self, donors=None):
        # Accepts only a list of donors now
        self.donors = donors

    def list_donor_names(self):
        donor_names = [donor.name for donor in self.donors]
        return ('\n'.join(donor_names))

    def add_donation(self, target_donor, new_donation):
        target_donor.add_donation(new_donation)
    
    def add_donor_and_donation(self, target_donor, new_donation):
        """ Called for a brand new donor only.  Creates new donor object """
        new_donor = Donor(target_donor, [new_donation])
        self.donors.append(new_donor)
        # self.add_donor(new_donor) --> deprecated
        print(f"{new_donor.name} has given {new_donor.donor_totals}")
    
    def send_thanks(self):
        """ Determines if the donor exists and gets the donation amount. """
        # Get donor
        target_donor = input("Please enter the donor's full name.  ")

        # Get donation
        try:
            new_donation = float(input("Please enter the donation amount for {}.  ".format(target_donor)))
        except ValueError:
            print("Please enter a number.  ")

        # Find donor or create and add new donor object.
        if target_donor in self.donors:
            self.add_donation(target_donor, new_donation)
        else:
            self.add_donor_and_donation(target_donor, new_donation)

        self.print_thanks(target_donor, new_donation)

    def print_thanks(self, target_donor, new_donation):
        message = f"""Dear {target_donor},
        Thank you for you generous donation of ${new_donation:.2f}.
        It will truly help the children.

        Sincerely,
        Donation Recievers"""
        print(message)

    def order_donors(self):
        """ 
        Orders the donors based on the sum of their total donations. 
        """
        ordered_donors = []
        for donor in self.donors:
            ordered_donors.append([donor])
        
        # Sorts on class default donor totals
        ordered_donors.sort(reverse=True)
        return ordered_donors
        
    def create_report(self):
        """ Prints a report based ordered by total donations. """
        # Base setup
        line_out = ''
        line_out += "Donor:                    | $    Total     |   Donations   | $   Average   |\n"
        line_out += ("-"*76) + '\n'
        
        # Setup line format to recieve ordered donor info 
        line_in = "{:<26}| ${:>14,.2f}|{:>15}| ${:>13,.2f}\n"
        ordered_donors = self.order_donors()

        # Donor object itself is contained in a list. [[donor1], [donor2]].  Peel that away to access properties.
        for info in ordered_donors:
            for donor in info: 
                line_out += line_in.format(donor.name, donor.donor_totals, donor.num_donations, donor.average_donations)

        print(line_out)

    def create_letters(self):
        """ Creates text files for each donor in the list. """
        for donor in self.donors:
            outletter = os.path.join(os.getcwd(), f'{donor.name}_ty_letter.txt')
            with open(outletter, 'w+') as f:
                message = f"""Dear {donor.name[0]},
                Thank you for you generous donation of ${donor.donor_totals:.2f}.
            It will truly help the children.


            Sincerely,
            Donation Receivers
        """
                f.write(message)

    def save_json(self):
        """ JSON formatted donor information. """
        # Convert to json compatible and use json built in to convert to str and write
        info = jsd._to_json_compat(self)
        with open('donors.json', 'w+') as outfile:
            json.dump(info, outfile)
    
    # @classmethod
    # def load_json(cls):
    #     """ Loads a JSON donor dictionary. """
    #     with open('donors.json', 'r') as infile:
    #         info = json.load(infile)
    #         formatted_info = jsd.from_json_dict(info)
    #         return formatted_info
    #     print(formatted_info)
    #     return formatted_info


    def load_json(self):
        """ Loads a JSON donor dictionary. """
        with open('donors.json', 'r') as infile:
            info = json.load(infile)
            formatted_info = jsd.from_json_dict(info)
        self.donors = formatted_info


    def quitter(self):
        print("Quitting.")
        quit()
    

def main():
    """ Controls the menu. """
    donor1 = Donor("Tom Horn", [599.23, 1000.00])
    donor2 = Donor("Theo Hartwell", [0.01, 0.01, 0.1])
    # donor3 = Donor("Bailey Kimmitt", [8723.22, 27167.22, 91817.66])
    # donor4 = Donor("Paul Hubbell", [90012.32, 2312.24])
    # donor5 = Donor("David Beckham", [1817266.11, 123123.66, 111335.112])
    # donors = DonorList([donor1, donor2, donor3, donor4, donor5])

    donors = DonorList([donor1, donor2])

    while True:
        choice = input(
        "Please select an option:\n\
        1 - Send Thanks\n\
        2 - Create Donor Report\n\
        3 - Send Letters\n\
        4 - Save Donors \n\
        5 - Load Donors \n\
        6 - Quit\n")
        print()
        if choice == '1':
            donors.send_thanks()
        if choice == '2':
            donors.create_report()
        if choice == '3':
            donors.create_letters()
        if choice == '4':
            donors.save_json()
        if choice == '5':
            donors.load_json()
        if choice == '6':
            donors.quitter()

if __name__ == "__main__":
    main()
