# Python imports
import json

class Emulator(object):
    """
    The emulator allow you to test complete Glass Application 
    without being part of Explorr Program
    """

    def __init__(self, app):
        self.app = app
        self.cards = []
        self.cards_new = []

    def post_card(self, card):
        """
        Insert card
        """
        card["id"] = len(self.cards)
        self.cards.append(card)
        self.cards_new.append(card)

    def _list_cards(self):
        """
        View for listing cards
        """
        return json.dumps(self.cards)

    def _list_cards_news(self):
        """
        View for listing cards
        """
        output = json.dumps(self.cards_new)
        self.cards_new = []
        return output

    def run(self):
        """
        Start the emulator
        """
        self.app.web.add_url_rule('/glass/emulator/list/cards/all', 'emulator_list_cards', self._list_cards)
        self.app.web.add_url_rule('/glass/emulator/list/cards/news', 'emulator_list_cards_news', self._list_cards_news)

