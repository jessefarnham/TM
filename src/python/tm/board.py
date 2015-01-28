import os

import json
import networkx as nx

from .common import CONF_DIR, Terrain, Element, Direction, TOWN_KEY_TEXTURE, POWER_TEXTURE


class SpaceCache(object):

    _id_to_space = {}
    _next_id = 0

    @classmethod
    def register(cls, space):
        cls._id_to_space[cls._next_id] = space
        id_for_space = cls._next_id
        cls._find_next_id()
        return id_for_space

    @classmethod
    def _find_next_id(cls):
        while cls._next_id in cls._id_to_space:
            cls._next_id += 1


class BoardEntity(object):

    def __init__(self, label, texture):
        self.label = label
        self.texture = texture


class BoardSpace(BoardEntity):

    def __init__(self, label=None, texture=None):
        super(BoardSpace, self).__init__(label, texture)
        self.space_id = SpaceCache.register(self)

    def __hash__(self):
        return hash(self.space_id)

    def __eq__(self, other):
        return self.space_id == other.space_id

    def __ne__(self, other):
        return not self.__eq__(other)


class BoardEdge(BoardEntity):

    def __init__(self, label=None, texture=None):
        super(BoardEdge, self).__init__(label, texture)


class MainBoardEdge(BoardEdge):

    def __init__(self, direction):
        super(MainBoardEdge, self).__init__()
        self.direction = direction


class MainBoardSpace(BoardSpace):

    def __init__(self, terrain):
        super(MainBoardSpace, self).__init__(texture=terrain.to_texture())
        self.terrain = terrain

    @classmethod
    def _from_conf(cls, conf_json):
        return cls(Terrain[conf_json['terrain']])


def _build_board_graph(json_obj):
    digraph = nx.DiGraph()
    for space_dict in json_obj['spaces']:
        space = MainBoardSpace._from_conf(space_dict)
        assert not digraph.has_node(space.space_id)
        digraph.add_node(space.space_id, space=space)
    for space_dict in json_obj['spaces']:
        for direction, neighbor_id in space_dict['neighbors'].items():
            assert space_dict['id'] != neighbor_id  # no self-loops
            edge = space_dict['id'], neighbor_id
            assert not digraph.has_edge(*edge)
            digraph.add_edge(*edge, edge=MainBoardEdge(Direction[direction]))

    # Check for no duplicate directions
    for node in digraph.nodes():
        directions = [data['edge'].direction for src, dest, data in digraph.edges(node, data=True)]
        assert len(set(directions)) == len(directions)

    # Check that all edges are bidirectional
    for src, dest in digraph.edges():
        assert digraph.has_edge(dest, src)
    return digraph


class CultBoardSpace(BoardSpace):

    def __init__(self, element, label):
        super(CultBoardSpace, self).__init__(texture=element.to_texture(), label=label)
        self.element = element


class CultProgressionSpace(CultBoardSpace):

    def __init__(self, element, level):
        super(CultProgressionSpace, self).__init__(element, label=level)
        self.level = level


class CultOrderSpace(CultBoardSpace):

    def __init__(self, element, advancement):
        super(CultOrderSpace, self).__init__(element, label=advancement)
        self.advancement = advancement


class CultLaneEdge(BoardEdge):

    def __init__(self, power=None, town_key=False):
        if town_key:
            texture = TOWN_KEY_TEXTURE
        else:
            texture = POWER_TEXTURE if power else None
        super(CultLaneEdge, self).__init__(label=power, texture=texture)
        self.power = power
        self.town_key = town_key


class Board(object):

    def __init__(self, digraph):
        self.digraph = digraph


class MainBoard(Board):

    def __init__(self):
        with open(os.path.join(CONF_DIR, 'board.json')) as json_stream:
            json_obj = json.load(json_stream)
        super(MainBoard, self).__init__(_build_board_graph(json_obj['mainBoard']))


def _build_cult_lane_digraph(element):
    digraph = nx.DiGraph()
    for i in range(10):
        digraph.add_node(i, space=CultProgressionSpace(element, i))
        digraph.add_node(i + 1, space=CultProgressionSpace(element, i + 1))
        if i == 2:
            power = 1
        elif i in (4, 6):
            power = 2
        elif i == 9:
            power = 3
        else:
            power = 0
        town_key = i == 9
        digraph.add_edge(i, i + 1, edge=CultLaneEdge(power, town_key))
    digraph.add_node(100, space=CultOrderSpace(element, 2))
    digraph.add_node(101, space=CultOrderSpace(element, 2))
    digraph.add_node(102, space=CultOrderSpace(element, 2))
    digraph.add_node(103, space=CultOrderSpace(element, 3))
    return digraph


class CultLane(Board):

    def __init__(self, element):
        self.element = element
        super(CultLane, self).__init__(_build_cult_lane_digraph(element))


class CultBoard(object):

    def __init__(self):
        self._lane = {}
        for element in Element:
            self._lane[element] = CultLane(element)

    def get_lane(self, element):
        return self._lane[element]
