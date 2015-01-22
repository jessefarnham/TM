import os

import json
import networkx

from .common import CONF_DIR, Terrain


class BoardSpace(object):

    def __init__(self, space_id, terrain):
        self.space_id = space_id
        self.terrain = terrain

    def __hash__(self):
        return hash(self.space_id)

    def __eq__(self, other):
        return self.space_id == other.space_id

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def from_conf(cls, conf_json):
        return cls(conf_json['id'], Terrain[conf_json['terrain']])


def _build_board_graph(json_obj):
    digraph = networkx.DiGraph()
    for space_dict in json_obj['spaces']:
        space = BoardSpace.from_conf(space_dict)
        assert not digraph.has_node(space.space_id)
        digraph.add_node(space.space_id, space=space)
    for space_dict in json_obj['spaces']:
        for direction, neighbor_id in space_dict['neighbors'].items():
            assert space_dict['id'] != neighbor_id  # no self-loops
            edge = space_dict['id'], neighbor_id
            assert not digraph.has_edge(*edge)
            digraph.add_edge(*edge, direction=direction)

    # Check for no duplicate directions
    for node in digraph.nodes():
        directions = [data['direction'] for src, dest, data in digraph.edges(node, data=True)]
        assert all([direction in ('NE', 'E', 'SE', 'SW', 'W', 'NW') for direction in directions])
        assert len(set(directions)) == len(directions)

    # Check that all edges are bidirectional
    for src, dest in digraph.edges():
        assert digraph.has_edge(dest, src)
    return digraph


class MainBoard(object):

    def __init__(self):
        with open(os.path.join(CONF_DIR, 'board.json')) as json_stream:
            json_obj = json.load(json_stream)
        self.digraph = _build_board_graph(json_obj['mainBoard'])
