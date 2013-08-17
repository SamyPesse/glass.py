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

    def post(self, **kwargs):
        """
        Post a card to glass timeline

        :param text: text content for the card
        :param html : html content for the card
        """
        if self.user.emulator:
            self.app.emulator_service.post_card(kwargs)
            return None
        
        # Not emulator
        card = self.user.session.post("/mirror/v1/timeline", data=json.dumps(kwargs)).json()
        
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
            print "template : %s" % output
            return self.post(html=output)