import random
import string
from src.client.client import Client
from src.models.models import DefaultContractData
from src.logger import logger
from starknet_py.contract import Contract


class Dmail:

    DMAIL_CONTRACT = DefaultContractData.DMAIL_CONTRACT.get('address')
    DMAIL_ABI = DefaultContractData.DMAIL_CONTRACT.get('abi')

    def __init__(self, client: Client):
        self.client = client
        self.contract = Contract(address=Dmail.DMAIL_CONTRACT, abi=Dmail.DMAIL_ABI, provider=self.client.account)

    async def send_message(self):
        try:
            logger.debug(
                f"[{self.client.address}] Sending message...[Dmail]")
            random_mail = self.generate_random_mail()
            random_text = self.generate_random_text()
            tx_hash = await self.client.send_transaction(interacted_contract=self.contract,
                                                         function_name='transaction',
                                                         to=random_mail,
                                                         theme=random_text)
            if tx_hash:
                logger.success(
                    f"[{self.client.address}] Successfully sent message {random_text} to {random_mail}| [Dmail]")
                return True
        except Exception as exc:
            logger.error(f"[{self.client.address}] Couldn't send message | [Dmail] | {exc}")
    @staticmethod
    def generate_random_mail():
        mail_domains = ['@gmx.com', '@gmail.com', '@dmail.ai']
        mail = ''
        symbols = [x for x in (string.ascii_lowercase + string.ascii_uppercase + str(string.digits))]
        for _ in range(5, random.randint(7, 15)):
            mail += random.choice(symbols)
        mail += random.choice(mail_domains)
        return mail

    @staticmethod
    def generate_random_text():
        text = ''
        subjects = ['I', 'You', 'We', 'They', 'He', 'She', 'It', 'People', 'Friends', 'Students',
                    'Teachers', 'Cats', 'Dogs', 'Birds', 'Fish', 'Parents', 'Siblings', 'Children', 'Artists',
                    'Musicians', 'Athletes', 'Scientists', 'Engineers', 'Doctors', 'Nurses', 'Farmers', 'Drivers',
                    'Chefs', 'Photographers', 'Writers', 'Explorers', 'Travellers', 'Singers', 'Dancers', 'Actors',
                    'Designers', 'Programmers', 'Hackers', 'Gamers', 'Readers', 'Listeners', 'Viewers', 'Dreamers',
                    'Thinkers', 'Believers', 'Disbelievers', 'Lovers', 'Haters', 'Strangers', 'Neighbors', 'Bosses',
                    'Employees', 'Leaders', 'Followers', 'Volunteers', 'Winners', 'Losers', 'Inventors', 'Innovators',
                    'Pioneers', 'Generations', 'Aliens', 'Robots', 'Monsters', 'Ghosts', 'Heroes', 'Villains', 'Kings',
                    'Queens', 'Princes', 'Princesses', 'Mermaids', 'Wizards', 'Fairies', 'Elves', 'Dwarves', 'Giants',
                    'Vampires', 'Werewolves', 'Zombies', 'Pirates', 'Superheroes', 'Supervillains', 'Time Travelers',
                    'Adventurers', 'Warriors', 'Scholars', 'Philosophers', 'Historians', 'Archaeologists', 'Detectives',
                    'Spies', 'Explorers', 'Astronauts', 'Cosmonauts', 'Soldiers', 'Refugees', 'Survivors', 'Migrants']

        verbs = ['run', 'eat', 'sleep', 'jump', 'laugh', 'cry', 'sing', 'dance', 'write', 'read',
                 'speak', 'think', 'dream', 'work', 'play', 'study', 'teach', 'learn', 'create', 'destroy',
                 'build', 'design', 'imagine', 'explore', 'discover', 'solve', 'question', 'answer', 'love',
                 'hate', 'like', 'dislike', 'trust', 'distrust', 'help', 'hurt', 'save', 'betray', 'forgive',
                 'forget', 'remember', 'achieve', 'fail', 'win', 'lose', 'fight', 'argue', 'cooperate', 'compete',
                 'travel', 'wander', 'conquer', 'submit', 'rebel', 'obey', 'challenge', 'adapt', 'change', 'grow',
                 'shrink', 'evolve', 'revolve', 'rotate', 'fall', 'rise', 'breathe', 'die', 'live', 'exist',
                 'vanish', 'appear', 'believe', 'doubt', 'convince', 'persuade', 'deceive', 'bet', 'swim', 'fly',
                 'crawl', 'walk', 'talk', 'whisper', 'shout', 'yell', 'whine', 'complain', 'request', 'demand',
                 'beg', 'steal', 'share', 'care', 'neglect', 'observe', 'watch', 'listen', 'hear', 'smell', 'taste']

        objects = ['apples', 'books', 'dogs', 'cars', 'clouds', 'flowers', 'mountains', 'oceans', 'stars', 'sand',
                   'rain', 'fire', 'ice', 'trees', 'birds', 'fish', 'food', 'water', 'air', 'earth', 'sun',
                   'moon', 'sky', 'rainbows', 'butterflies', 'raindrops', 'snowflakes', 'waves', 'rocks', 'stones',
                   'shadows', 'mirrors', 'dreams', 'thoughts', 'emotions', 'memories', 'colors', 'sounds', 'smells',
                   'tastes', 'touch', 'love', 'hate', 'friendship', 'family', 'society', 'culture', 'nature',
                   'technology',
                   'art', 'music', 'movies', 'books', 'games', 'sports', 'knowledge', 'wisdom', 'beauty', 'truth',
                   'lies', 'hope', 'fear', 'joy', 'sadness', 'anger', 'happiness', 'conflict', 'peace', 'war',
                   'freedom', 'imprisonment', 'equality', 'inequality', 'justice', 'injustice', 'faith', 'doubt',
                   'religion',
                   'science', 'magic', 'dreams', 'nightmares', 'heroes', 'villains', 'dreamlands', 'night', 'day',
                   'past', 'future', 'present', 'infinity', 'space', 'time', 'dreamscapes', 'horizons', 'destinations']
        all_words = objects + verbs + subjects
        for _ in range(1, random.randint(2, 4)):
            text += random.choice(all_words).lower()
            text += ' '
        return text
