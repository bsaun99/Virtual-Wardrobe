import pytest
import db.contacts as cnt

def test_get_contacts():
    cnts = cnt.get_contacts()
    assert isinstance(cnts, list)
    assert len(cnts)>1

def test_get_contacts_dict():
    cnts = cnt.get_contacts_dict()
    assert isinstance(cnts, dict)
    assert len(cnts) > 1

def test_get_contact_details():
    cnt_dets = cnt.get_contacts_details(cnt.TEST_USER_NAME)
    assert isinstance(cnt_dets, dict)



def test_add_contact():
    details = {}
    for field in cnt.REQUIRED_FLDS:
        details[field] = 2
    cnt.add_contact(cnt.TEST_USER_NAME, details)