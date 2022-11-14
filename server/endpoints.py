"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask, request
from flask_restx import Resource, Api, fields, Namespace
import werkzeug.exceptions as wz

import db.char_types as ctyp
import db.games as gm
import db.users as usr
import db.closet_browse as brwse

app = Flask(__name__)
api = Api(app)

CHAR_TYPES_NS = 'character_types'
LOGIN_NS = 'login'
GAMES_NS = 'games'
USERS_NS = 'users'
CLOSETBROWSE_NS = 'closet_broswe'

char_types = Namespace(CHAR_TYPES_NS, 'Character Types')
api.add_namespace(char_types)
games = Namespace(GAMES_NS, 'Games')
api.add_namespace(games)
login = Namespace(LOGIN_NS, 'Login')
api.add_namespace(login)
users = Namespace(USERS_NS, 'Users')
api.add_namespace(users)
closet_browse = Namespace(CLOSETBROWSE_NS, 'Closet Browse')
api.add_namespace(closet_browse)

LIST = 'list'
DICT = 'dict'
DETAILS = 'details'
ADD = 'add'
MAIN_MENU = '/main_menu'
MAIN_MENU_NM = 'Main Menu'
HELLO = '/hello'
MESSAGE = 'message'
CHAR_TYPE_DICT = f'/{DICT}'
CHAR_TYPE_DICT_W_NS = f'{CHAR_TYPES_NS}/{DICT}'
CHAR_TYPE_DICT_NM = f'{CHAR_TYPES_NS}_dict'
CHAR_TYPE_LIST = f'/{LIST}'
CHAR_TYPE_LIST_W_NS = f'{CHAR_TYPES_NS}/{LIST}'
CHAR_TYPE_LIST_NM = f'{CHAR_TYPES_NS}_list'
CHAR_TYPE_DETAILS = f'/{DETAILS}'
CHAR_TYPE_DETAILS_W_NS = f'{CHAR_TYPES_NS}/{DETAILS}'
GAME_DICT = f'/{DICT}'
GAME_DICT_W_NS = f'{GAMES_NS}/{DICT}'
GAME_DETAILS = f'/{DETAILS}'
GAME_DETAILS_W_NS = f'{GAMES_NS}/{DETAILS}'
GAME_ADD = f'/{GAMES_NS}/{ADD}'
USER_DICT = f'/{DICT}'
USER_DICT_W_NS = f'{USERS_NS}/{DICT}'
USER_DICT_NM = f'{USERS_NS}_dict'
USER_LIST = f'/{LIST}'
USER_LIST_W_NS = f'{USERS_NS}/{LIST}'
USER_LIST_NM = f'{USERS_NS}_list'
USER_DETAILS = f'/{USERS_NS}/{DETAILS}'
USER_ADD = f'/{USERS_NS}/{ADD}'
CLOSETBROWSE_DICT = f'/{DICT}'
CLOSETBROWSE_DICT_W_NS = f'{CLOSETBROWSE_NS}/{DICT}'
CLOSETBROWSE_DICT_NM = f'{CLOSETBROWSE_NS}_dict'
CLOSETBROWSE_LIST = f'/{LIST}'
CLOSETBROWSE_LIST_W_NS = f'{CLOSETBROWSE_NS}/{LIST}'
CLOSETBROWSE_LIST_NM = f'{CLOSETBROWSE_NS}_list'
CLOSETBROWSE_DETAILS = f'/{CLOSETBROWSE_NS}/{DETAILS}'
CLOSETBROWSE_ADD = f'/{CLOSETBROWSE_NS}/{ADD}'


@api.route(HELLO)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """

    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {MESSAGE: 'hello world'}


@api.route(MAIN_MENU)
class MainMenu(Resource):
    """
    This will deliver our main menu.
    """
    def get(self):
        """
        Gets the main game menu.
        """
        return {'Title': MAIN_MENU_NM,
               'Default': 2,
               'Choices': {
                   '1': {'url': f'/{LOGIN_NS}',
                         'method': 'post', 'text': 'Login'},
                   '2': {'url': f'/{USER_DICT_W_NS}',
                         'method': 'get', 'text': 'List Users'},
                   '3': {'url': f' / {CLOSETBROWSE_DICT_W_NS}',
                          'method': 'get', 'text': 'List Clothes Available to Browse'},
                   'X': {'text': 'Exit'},
                }}


@char_types.route(CHAR_TYPE_LIST)
class CharacterTypeList(Resource):
    """
    This will get a list of character types.
    """

    def get(self):
        """
        Returns a list of character types.
        """
        return {CHAR_TYPE_LIST_NM: ctyp.get_char_types()}


@char_types.route(CHAR_TYPE_DICT)
class CharacterTypeDict(Resource):
    """
    This will get a list of character types.
    """

    def get(self):
        """
        Returns a list of character types.
        """
        return {'Data': ctyp.get_char_type_dict(),
                'Type': 'Data',
                'Title': 'Character Types'}


@char_types.route(f'{CHAR_TYPE_DETAILS}/<char_type>')
class CharacterTypeDetails(Resource):
    """
    This will return details on a character type.
    """

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, char_type):
        """
        This will return details on a character type.
        """
        ct = ctyp.get_char_type_details(char_type)
        if ct is not None:
            return {char_type: ctyp.get_char_type_details(char_type)}
        else:
            raise wz.NotFound(f'{char_type} not found.')



@games.route(f'{GAME_DETAILS}/<game>')
class GameDetails(Resource):
    """
    This will get details on a game.
    """

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, game):
        """
        Returns a list of character types.
        """
        ct = gm.get_game_details(game)
        if ct is not None:
            return {game: gm.get_game_details(game)}
        else:
            raise wz.NotFound(f'{game} not found.')


game_fields = api.model('NewGame', {
    gm.NAME: fields.String,
    gm.NUM_PLAYERS: fields.Integer,
    gm.LEVEL: fields.Integer,
    gm.VIOLENCE: fields.Integer,
})


@api.route(GAME_ADD)
class AddGame(Resource):
    """
    Add a game.
    """

    @api.expect(game_fields)
    def post(self):
        """
        Add a game.
        """
        print(f'{request.json}')
        name = request.json[gm.NAME]
        del request.json[gm.NAME]
        gm.add_game(name, request.json)


@users.route(USER_DICT)
class UserDict(Resource):
    """
    This will get a list of currrent users.
    """

    def get(self):
        """
        Returns a list of current users.
        """
        return {'Data': usr.get_users_dict(),
                'Type': 'Data',
                'Title': 'Active Users'}


@users.route(USER_LIST)
class UserList(Resource):
    """
    This will get a list of currrent users.
    """

    def get(self):
        """
        Returns a list of current users.
        """
        return {USER_LIST_NM: usr.get_users()}


user_fields = api.model('Username', {
    usr.USERNAME: fields.String,
    usr.PASSWORD: fields.String
})


@api.route(USER_ADD)
class AddUser(Resource):
    """
    Add a user.
    """

    @api.expect(user_fields)
    def post(self):
        """
        Add a user.
        """
        print(f'{request.json}')
        name = request.json[usr.NAME]
        del request.json[usr.NAME]
        usr.add_user(name, request.json)


@closet_browse.route(CLOSETBROWSE_DICT)
class ClosetList(Resource):
    """
    This will get a list of currrent clothing items in the closet inventory.
    """
    def get(self):
        """
        Returns a list of current clothing items.
        """
        return {'Data': brwse.get_clothing_dict(),
                'Type': 'Data',
                'Title': 'Available Clothes'}


@closet_browse.route(f'{CLOSETBROWSE_DETAILS}/<item>')
class ClosetDetails(Resource):
    """
    This will get details on a clothing item.
    """

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, clothing):
        """
        Returns a list of clothing category types.
        """
        cb = brwse.get_clothing_details(clothing)
        if cb is not None:
            return {clothing: brwse.get_clothing_details(clothing)}
        else:
            raise wz.NotFound(f'{clothing} not found.')


closet_browse_fields = api.model('NewClothing', {
    brwse.CATEGORY: fields.String,
    brwse.SEASON: fields.String,
    brwse.OCCASION: fields.String,
    brwse.AESTHETIC: fields.String,
    brwse.RANDOM: fields.String,
})


@api.route(CLOSETBROWSE_ADD)
class AddClothing(Resource):
    """
    Add a clothing item.
    """

    @api.expect(closet_browse_fields)
    def post(self):
        """
        Add a clothing item to closet.
        """
        print(f'{request.json=}')
        item = request.json[brwse.CLOTHING]
        del request.json[brwse.CLOTHING]
        brwse.add_clothing(item, request.json)

@api.route('/endpoints')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """

    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = ''
        # sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}
