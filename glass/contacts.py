# Python imports
import os
import json

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
        r = self.user.session.get("/mirror/v1/contacts/%s" % (contactid))
        contact = r.json()
        
        if (contact is None or not "id" in contact):
            raise Exception("Error getting contact ", contact)
        return contact

    def delete(self, contactid):
        """
        Delete a contact
        ref: https://developers.google.com/glass/v1/reference/contacts/delete
        """
        r = self.user.session.delete("/mirror/v1/contacts/%s" % (contactid))
        r.raise_for_status()

    def patch(self, contactid, **kwargs):
        """
        Patch a contact
        ref: https://developers.google.com/glass/v1/reference/contacts/patch
        """
        r = self.user.session.patch("/mirror/v1/contacts/%s" % (contactid), data=json.dumps(kwargs))
        contact = r.json()
        
        if (contact is None or not "id" in contact):
            raise Exception("Error patching contact ", contact)
        return contact

    def list(self, **kwargs):
        """
        List contacts
        ref: https://developers.google.com/glass/v1/reference/contacts/list
        """
        r = self.user.session.get("/mirror/v1/contacts", data=kwargs)
        contacts = r.json()
        
        if (contacts is None or not "items" in contacts):
            raise Exception("Error listing contacts ", contacts)
        return contacts["items"]

    def insert(self, **kwargs):
        """
        Insert a new contact
        ref: https://developers.google.com/glass/v1/reference/contacts/insert
        """
        r = self.user.session.post("/mirror/v1/contacts", data=json.dumps(kwargs))
        contact = r.json()
        
        if (contact is None or not "id" in contact):
            raise Exception("Error inserting contact", contact)
        return contact
