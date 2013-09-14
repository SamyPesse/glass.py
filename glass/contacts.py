# Python imports
import os
import json

# Local imports
import exceptions

class Contacts(object):
    """
    Represent contacts for a user
    """

    def __init__(self, user):
        self.user = user
        self.app = user.app

    def get(self, contactid):
        """
        Get a contact
        ref: https://developers.google.com/glass/v1/reference/contacts/get
        """
        r = self.user.request("GET", "/mirror/v1/contacts/%s" % (contactid))
        contact = r.json()
        
        if (contact is None or not "id" in contact):
            raise exceptions.ContactException("Error getting contact ", contact)
        return contact

    def delete(self, contactid):
        """
        Delete a contact
        ref: https://developers.google.com/glass/v1/reference/contacts/delete
        """
        r = self.user.request("DELETE", "/mirror/v1/contacts/%s" % (contactid))

    def patch(self, contactid, **kwargs):
        """
        Patch a contact
        ref: https://developers.google.com/glass/v1/reference/contacts/patch
        """
        r = self.user.request("PATCH", "/mirror/v1/contacts/%s" % (contactid), data=json.dumps(kwargs))
        contact = r.json()
        
        if (contact is None or not "id" in contact):
            raise exceptions.ContactException("Error patching contact ", contact)
        return contact

    def list(self, **kwargs):
        """
        List contacts
        ref: https://developers.google.com/glass/v1/reference/contacts/list
        """
        r = self.user.request("GET", "/mirror/v1/contacts", data=kwargs)
        contacts = r.json()
        
        if (contacts is None or not "items" in contacts):
            raise exceptions.ContactException("Error listing contacts ", contacts)
        return contacts["items"]

    def insert(self, **kwargs):
        """
        Insert a new contact
        ref: https://developers.google.com/glass/v1/reference/contacts/insert
        """
        r = self.user.request("POST", "/mirror/v1/contacts", data=json.dumps(kwargs))
        contact = r.json()
        
        if (contact is None or not "id" in contact):
            raise exceptions.ContactException("Error inserting contact", contact)
        return contact
