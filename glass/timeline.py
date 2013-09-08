# Python imports
import os
import json
from jinja2 import Template

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
        r = self.user.session.get("/mirror/v1/timeline/%s" % (cardid))
        card = r.json()
        
        if (card is None or not "id" in card):
            raise Exception("Error getting card from timeline ", card)
        return card

    def delete(self, cardid):
        """
        Delete a card from the timeline
        ref: https://developers.google.com/glass/v1/reference/timeline/get
        """
        r = self.user.session.delete("/mirror/v1/timeline/%s" % (cardid))
        r.raise_for_status()

    def patch(self, cardid,**kwargs):
        """
        Delete a card from the timeline
        ref: https://developers.google.com/glass/v1/reference/timeline/get
        """
        r = self.user.session.patch("/mirror/v1/timeline/%s" % (cardid), data=json.dumps(kwargs))
        card = r.json()
        
        if (card is None or not "id" in card):
            raise Exception("Error patching card in timeline ", card)
        return card

    def list(self, **kwargs):
        """
        List cards in the timeline
        ref: https://developers.google.com/glass/v1/reference/timeline/list
        """
        r = self.user.session.get("/mirror/v1/timeline", data=kwargs)
        cards = r.json()
        
        if (cards is None or not "items" in cards):
            raise Exception("Error listing cards in timeline ", cards)
        return cards["items"]

    def post(self, **kwargs):
        """
        Post a card to glass timeline
        ref: https://developers.google.com/glass/v1/reference/timeline/insert

        :param text: text content for the card
        :param html : html content for the card
        """
        if self.user.emulator:
            self.app.emulator_service.post_card(kwargs)
            return None
        
        # Not emulator
        r = self.user.session.post("/mirror/v1/timeline", data=json.dumps(kwargs))
        card = r.json()
        
        if (card is None or not "id" in card):
            raise Exception("Error posting card to timeline ", card)
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
            return self.post(html=output)