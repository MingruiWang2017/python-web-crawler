import logging

from twisted.internet import defer, protocol, reactor


class CommandSolt(protocol.ProcessProtocol):
    """A ProcessProtocol that sends prices through a binary"""

    def __init__(self, args):
        """初始化成员变量，并启动一个新进程"""
        self._current_deferred = None
        