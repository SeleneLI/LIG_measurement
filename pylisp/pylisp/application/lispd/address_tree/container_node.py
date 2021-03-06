'''
Created on 11 mrt. 2013

@author: sander
'''
from ipaddress import ip_network
from pylisp.application.lispd.address_tree.base import AbstractNode, MoreSpecificsFoundError, NotAuthoritativeError
import logging


# Get the logger
logger = logging.getLogger(__name__)


class ContainerNode(AbstractNode):
    def __init__(self, prefix, children=None):
        super(ContainerNode, self).__init__(prefix)
        self.children = set()

        if children:
            self.update(children)

    def set_sockets(self, control_plane_sockets, data_plane_sockets):
        super(ContainerNode, self).set_sockets(control_plane_sockets, data_plane_sockets)

        for child in self.children:
            child.set_sockets(control_plane_sockets, data_plane_sockets)

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.prefix,
                               self.children)

    def __iter__(self):
        return iter(self.children)

    def __len__(self):
        return len(self.children)

    def resolve_path(self, address):
        '''
        Resolve the given address in this tree branch
        '''
        match = self.find_one(address)
        if not match:
            return [self]

        # Go further up the tree if possible
        if isinstance(match, ContainerNode):
            return match.resolve_path(address) + [self]

        # This is as far as we go
        return [match, self]

    def resolve(self, address):
        return self.resolve_path(address)[0]

    def find_one(self, address):
        '''
        Find the given address or prefix
        '''
        # Convert to a network and find all matches
        prefix = ip_network(address)
        matches = self.find_all(prefix)

        if not matches:
            # Nothing found
            return None

        if len(matches) > 1:
            # Found too much
            raise MoreSpecificsFoundError('Found more-specifics for %r' % prefix)

        # One match is what we want
        match = matches.pop()

        # The match should completely contain the prefix we look for
        if match.prefix[0] <= prefix[0] and match.prefix[-1] >= prefix[-1]:
            return match

    def find_exact(self, prefix):
        '''
        Find the exact child with the given prefix
        '''
        matches = self.find_all(prefix)
        if len(matches) == 1:
            match = matches.pop()
            if match.prefix == prefix:
                return match

        return None

    def find_all(self, prefix):
        '''
        Find everything in the given prefix
        '''
        prefix = ip_network(prefix)

        # Check that we are authoritative for the given prefix
        if not self.prefix.overlaps(prefix) \
        or self.prefix[0] > prefix[0] \
        or self.prefix[-1] < prefix[-1]:
            raise NotAuthoritativeError('This node is not authoritative for %r'
                                        % prefix)

        # Find all matching existing prefixes and return them in a set
        matches = set()
        for child in self.children:
            if prefix.overlaps(child.prefix):
                matches.add(child)

        return matches

    def add(self, child):
        assert isinstance(child, AbstractNode)

        # Check that we are authoritative for the child
        if not self.prefix.overlaps(child.prefix) \
        or self.prefix[0] > child.prefix[0] \
        or self.prefix[-1] < child.prefix[-1]:
            raise NotAuthoritativeError('This node is not authoritative for %r'
                                        % child.prefix)

        # Check for overlap, but ignore exact an match and overwrite it
        if not self.find_exact(child.prefix):
            matches = self.find_all(child.prefix)
            if matches:
                raise ValueError('New prefix %r overlaps with existing '
                                 'prefixes' % child.prefix)

        # Add the new child
        self.children.add(child)

    def clear(self):
        self.children = set()

    def __contains__(self, child):
        # If a node is given then directly look for it
        if isinstance(child, AbstractNode):
            return child in self.children

        # Also allow to find a node by network
        match = self.find_exact(child)
        return bool(match)

    def copy(self):
        return self.__class__(self.prefix, self.children)

    def discard(self, child):
        # If a node is given then directly discard it
        if isinstance(child, AbstractNode):
            self.children.discard(child)
            return

        # Also allow to discard a node by network
        match = self.find_exact(child)
        if match:
            self.children.discard(match)

    def remove(self, child):
        orig_len = len(self)
        self.discard(child)
        if len(self) != orig_len:
            raise KeyError(child)

    def update(self, children):
        for child in children:
            self.add(child)
