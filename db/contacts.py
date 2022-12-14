'''
This module encapsulates contact requests from the user.
'''

TEST_USER_NAME = 'Test User'
TEST_FIRST_NAME = 'Jane'
TEST_LAST_NAME = 'Doe'
FULL_NAME = 'full_name'
FIRST_NAME = 'first_name'
LAST_NAME = 'last_name'
EMAIL = 'email'
REQUEST = 'request'
REQUIRED_FLDS = [FIRST_NAME, LAST_NAME, EMAIL, REQUEST]
contacts = {TEST_USER_NAME: {EMAIL: 'x@y.com',
                             FULL_NAME: TEST_FIRST_NAME + ' ' + TEST_LAST_NAME,
                             REQUEST: []},
            'Test User 2': {EMAIL: 'z@y.com',
                            FULL_NAME: 'John Doe', REQUEST: []}}


def add_contact(name, details):
    if not isinstance(name, str):
        raise TypeError(f'Wrong type for name: {type(name)=}')
    if not isinstance(details, dict):
        raise TypeError(f'Wrong type for details: {type(details)=}')
    for field in REQUIRED_FLDS:
        if field not in details:
            raise ValueError(f'Required {field=} missing from details.')
    contacts[name] = details


def get_contacts():
    return list(contacts.keys())


def get_contacts_dict():
    return contacts


def get_contact_details(user):
    return contacts.get(user, None)


def del_contact(name):
    del contacts[name]


def add_request(user, request):
    contacts[user][REQUEST].append(request)


def get_request(user):
    return contacts.get(user, None)


def main():
    contacts = get_contacts()
    print(f'{contacts=}')
    print(f'{get_contact_details(TEST_USER_NAME)=}')
