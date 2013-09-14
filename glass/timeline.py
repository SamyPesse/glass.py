# Python imports
import os
import json
from jinja2 import Template

# Local imports
import exceptions

class Timeline(object):
    """
    Represent an user timeline

    Post to timeline using : timeline.post
    examples :
        timeline.post(text="Hello World")
    """

    def __init__(self, user):
        self.user = user
        self.app = user.app

    def get(self, cardid):
        """
        Get a card from the timeline
        ref: https://developers.google.com/glass/v1/reference/timeline/get
        """
        r = self.user.request("GET", "/mirror/v1/timeline/%s" % (cardid))
        card = r.json()
        
        if (card is None or not "id" in card):
            raise exceptions.TimelineException("Error getting card from timeline ", card)
        return card

    def delete(self, cardid):
        """
        Delete a card from the timeline
        ref: https://developers.google.com/glass/v1/reference/timeline/get
        """
        r = self.user.request("DELETE", "/mirror/v1/timeline/%s" % (cardid))

    def patch(self, cardid, **kwargs):
        """
        Patch a card in the timeline
        ref: https://developers.google.com/glass/v1/reference/timeline/get
        """
        r = self.user.request("PATCH", "/mirror/v1/timeline/%s" % (cardid), data=json.dumps(kwargs))
        card = r.json()
        
        if (card is None or not "id" in card):
            raise exceptions.TimelineException("Error patching card in timeline ", card)
        return card

    def list(self, **kwargs):
        """
        List cards in the timeline
        ref: https://developers.google.com/glass/v1/reference/timeline/list
        """
        r = self.user.request("GET", "/mirror/v1/timeline", data=kwargs)
        cards = r.json()
        
        if (cards is None or not "items" in cards):
            raise exceptions.TimelineException("Error listing cards in timeline ", cards)
        return cards["items"]

    def post(self, **kwargs):
        """
        Post a card to glass timeline
        ref: https://developers.google.com/glass/v1/reference/timeline/insert

        :param text: text content for the card
        :param html : html content for the card
        """
        r = self.user.request("POST", "/mirror/v1/timeline", data=json.dumps(kwargs))
        card = r.json()
        
        if (card is None or not "id" in card):
            raise exceptions.TimelineException("Error posting card to timeline ", card)
        return card

    def post_template(self, template, **kwargs):
        """
        Post a card with an html template

        :param template: name of the template
        """
        path = os.path.join(self.app.template_folder, template)
        with open(path, "r") as templatefile:
            template = Template(templatefile.read())
            output = template.render(**kwargs)
            print output
            return self.post(html=output)
