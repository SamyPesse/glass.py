# Python imports
import json

class Timeline(object):
    """
    Represent an user timeline

    Post to timeline using : timeline.post
    examples :
    	timeline.post(text="Hello World")
    """

    def __init__(self, user):
        self.user = user

    def post(self, **kwargs):
        """
        Post a card to glass timeline

        :param text: text content for the card
        :param html : html content for the card
        """
        card = self.user.session.post("/mirror/v1/timeline", data=json.dumps(kwargs)).json()
        
        if (card is None or not "id" in card):
            raise Exception("Error posting card to timeline ", card)
        return card