# -*- coding: utf-8 -*-
# @Time    : 2020-04-23 00:10
# @Author  : li
# @File    : message.py


from abc import abstractmethod
from typing import Any, Iterator
from sprite.utils.args import Args
from sprite.core.download.xfer import XferPipe
from sprite.core.download.codec import NONE_CODEC_ID, CodecMap
from sprite.const import STATUS_OK
from sprite.utils.utils import random_seq


class BaseHeader:

    def __init__(self, msg_type: 'str', service_method: 'str', meta: 'Args', seq: 'str' = None):
        """
        :param msg_type: 消息类型
        :param service_method: 调用方法路径
        :param meta: 元信息对象
        """
        self.__seq = random_seq() if not seq else seq
        self.__status = STATUS_OK
        self.__msg_type = msg_type
        self.__service_method = service_method
        self.__meta = meta

    @abstractmethod
    def seq(self) -> 'str':
        """
        返回message的编号
        :return:
        """

    # @abstractmethod
    # def set_seq(self, seq: 'int'):
    #     """
    #     设置消息的编号
    #     :param seq:
    #     :return:
    #     """

    @abstractmethod
    def msg_type(self) -> 'str':
        """
        返回消息类型
        :return:
        """

    # @abstractmethod
    # def set_mtype(self, mtype: 'str'):
    #     """
    #     设置消息类型
    #     :param mtype:
    #     :return:
    #     """

    @abstractmethod
    def service_method(self) -> 'str':
        """
        返回服务方法
        :return:
        """

    # @abstractmethod
    # def set_service_method(self, service_method: 'str'):
    #     """
    #     设置服务方法
    #     :param service_method:
    #     :return:
    #     """

    @abstractmethod
    def status_ok(self) -> 'bool':
        """
        返回消息是否ok
        :return:
        """

    @abstractmethod
    def status(self) -> 'int':
        """
        返回消息状态
        :return:
        """

    # @abstractmethod
    # def set_status(self, status: 'int'):
    #     """
    #     设置状态
    #     :param status:
    #     :return:
    #     """

    @abstractmethod
    def meta(self) -> 'Args':
        """
        返回message的元信息
        :return:
        """


class BaseBody:

    def __init__(self, body_codec: 'int', body: 'Any' = None):
        self.__body = body
        self.__body_codec = body_codec

    @abstractmethod
    def body_codec(self) -> 'int':
        """
        返回body的序列化器的编号
        :return:
        """

    # @abstractmethod
    # def set_body_codec(self, body_codec: 'int'):
    #     """
    #     设置body的序列化器编号
    #     :param body_codec:
    #     :return:
    #     """

    @abstractmethod
    def body(self) -> 'Any':
        """
        返回body
        :return:
        """

    # @abstractmethod
    # def set_body(self, body: 'Any'):
    #     """
    #     设置body
    #     :param body:
    #     :return:
    #     """

    @abstractmethod
    def marshal_body(self) -> 'bytes':
        """
        将body序列化
        :return:
        """

    @abstractmethod
    def un_marshal_body(self, body_bytes: 'bytes'):
        """
        反序列化得到body
        :param body_bytes:
        :return:
        """


def check_message_size(size: 'int'):
    pass


class Message(BaseHeader, BaseBody):
    def __init__(self, service_method: 'str', msg_type: 'str', meta: 'Args', body_codec: 'int',
                 body: 'Any' = None, xfer_pipe: 'XferPipe' = None, seq: 'str' = None):
        self.__xfer_pipe = xfer_pipe
        self.__size = 0

        self._raw_resp = b''
        BaseHeader.__init__(self, service_method, msg_type, meta, seq)
        BaseBody.__init__(self, body_codec, body)

    @property
    def seq(self) -> 'str':
        return self.__seq

    @property
    def msg_type(self):
        return self.__msg_type

    @property
    def service_method(self):
        return self.__service_method

    def status_ok(self) -> 'bool':
        return self.__status == STATUS_OK

    @property
    def status(self) -> 'int':
        return self.__status

    @property
    def meta(self) -> 'Args':
        return self.__meta

    @property
    def body_codec(self) -> 'int':
        return self._body_codec

    def set_body_codec(self, body_codec: 'int'):
        self._body_codec = body_codec

    @property
    def body(self) -> 'Any':
        return self.__body

    def marshal_body(self) -> 'bytes':
        if self.__body is None:
            return bytes()
        return CodecMap.marshal(self.__body_codec, self.__body)

    def un_marshal_body(self, body_bytes: 'bytes') -> 'Any':
        if len(body_bytes) == 0:
            return None
        return CodecMap.un_marshal(self.__body_codec, body_bytes)

    @property
    def xfer_pipe(self) -> 'XferPipe':
        return self.__xfer_pipe

    @property
    def size(self) -> 'int':
        return self.__size

    def __str__(self):
        return ""

    @staticmethod
    def with_nothing():
        def decorate_nothing(message: 'Message'):
            pass

        return decorate_nothing

    @staticmethod
    def with_service_method(service_method: 'str'):
        def decorate_service_method(message: 'Message'):
            message.set_service_method(service_method)

        return decorate_service_method

    @staticmethod
    def with_status(status: 'int'):
        def decorated_status(message: 'Message'):
            message.set_status(status)

        return decorated_status

    @staticmethod
    def with_add_meta(key: 'str', value: 'str'):
        def decorated_add_meta(message: 'Message'):
            message.meta[key] = value

        return decorated_add_meta

    @staticmethod
    def with_set_meta(key: 'str', value: 'str'):
        def decorated_set_meta(message: 'Message'):
            message.meta[key] = value

        return decorated_set_meta

    @staticmethod
    def with_del_meta(key: 'str'):
        def decorated_del_meta(message: 'Message'):
            del message.meta[key]

        return decorated_del_meta

    @staticmethod
    def with_body_codec(body_codec: 'int'):
        def decorated_body_codec(message: 'Message'):
            message.set_body_codec(body_codec)

        return decorated_body_codec

    @staticmethod
    def with_body(body: 'Any'):
        def decorated_body(message: 'Message'):
            message.set_body_codec(body)

        return decorated_body

    @staticmethod
    def with_xfer_pipe(filter_id: 'Iterator'):
        def decorated_xfer_pipe(message: 'Message'):
            message.xfer_pipe.append(filter_id)

        return decorated_xfer_pipe


# class Message(BaseHeader, BaseBody):
#     def __init__(self, http_method: 'str' = "", service_method: 'str' = "", seq: 'int' = 0, meta: 'Args' = None,
#                  mtype: 'str' = "call", body: 'Any' = None, body_codec: 'int' = NONE_CODEC_ID):
#         """
#         :param http_method: http协议类型
#         :param service_method: uri
#         :param seq: 消息编号
#         :param meta:
#         :param mtype:
#         :param body:
#         :param body_codec:
#         """
#         self._http_method = http_method
#         self._service_method = service_method
#         self._status = 0
#         self._meta = meta or Args()
#         assert isinstance(self._meta, Args), "meta must Args instance"
#         self._body = body
#         self._xfer_pipe = XferPipe()
#         self._size = 0
#         self._seq = seq
#         self._mtype = mtype
#         self._body_codec = body_codec
#
#     def reset(self, service_method: 'str' = "", seq: 'int' = 0,
#               mtype: 'str' = "", body: 'Any' = None, body_codec: 'int' = NONE_CODEC_ID):
#         self._service_method = service_method
#         self._status = 0
#         self._meta.reset()
#         self._body = body
#         self._xfer_pipe.reset()
#         self._size = 0
#         self._seq = seq
#         self._mtype = mtype
#         self._body_codec = body_codec
#
#     @property
#     def http_method(self) -> 'str':
#         return self._http_method
#
#     @property
#     def seq(self) -> 'int':
#         return self._seq
#
#     def set_seq(self, seq: 'int'):
#         self._seq = seq
#
#     @property
#     def mtype(self):
#         return self._mtype
#
#     def set_mtype(self, mtype: 'str'):
#         self._mtype = mtype
#
#     @property
#     def service_method(self):
#         return self._service_method
#
#     def set_service_method(self, service_method: 'str'):
#         self._service_method = service_method
#
#     def status_ok(self) -> 'bool':
#         return self._status == STATUS_OK
#
#     @property
#     def status(self) -> 'int':
#         return self._status
#
#     def set_status(self, status: 'int'):
#         self._status = status
#
#     @property
#     def meta(self) -> 'Args':
#         return self._meta
#
#     @property
#     def body_codec(self) -> 'int':
#         return self._body_codec
#
#     def set_body_codec(self, body_codec: 'int'):
#         self._body_codec = body_codec
#
#     @property
#     def body(self) -> 'Any':
#         return self._body
#
#     def set_body(self, body: 'Any'):
#         self._body = body
#
#     def marshal_body(self) -> 'bytes':
#         if self._body is None:
#             return bytes()
#         return CodecMap.marshal(self._body_codec, self._body)
#
#     def un_marshal_body(self, body_bytes: 'bytes') -> 'Any':
#         if len(body_bytes) == 0:
#             return None
#         return CodecMap.un_marshal(self._body_codec, body_bytes)
#
#     @property
#     def xfer_pipe(self) -> 'XferPipe':
#         return self._xfer_pipe
#
#     @property
#     def size(self) -> 'int':
#         return self._size
#
#     def set_size(self, size: 'int'):
#         check_message_size(size)
#         self._size = size
#
#     def __str__(self):
#         return ""
#
#     @staticmethod
#     def with_nothing():
#         def decorate_nothing(message: 'Message'):
#             pass
#
#         return decorate_nothing
#
#     @staticmethod
#     def with_service_method(service_method: 'str'):
#         def decorate_service_method(message: 'Message'):
#             message.set_service_method(service_method)
#
#         return decorate_service_method
#
#     @staticmethod
#     def with_status(status: 'int'):
#         def decorated_status(message: 'Message'):
#             message.set_status(status)
#
#         return decorated_status
#
#     @staticmethod
#     def with_add_meta(key: 'str', value: 'str'):
#         def decorated_add_meta(message: 'Message'):
#             message.meta[key] = value
#
#         return decorated_add_meta
#
#     @staticmethod
#     def with_set_meta(key: 'str', value: 'str'):
#         def decorated_set_meta(message: 'Message'):
#             message.meta[key] = value
#
#         return decorated_set_meta
#
#     @staticmethod
#     def with_del_meta(key: 'str'):
#         def decorated_del_meta(message: 'Message'):
#             del message.meta[key]
#
#         return decorated_del_meta
#
#     @staticmethod
#     def with_body_codec(body_codec: 'int'):
#         def decorated_body_codec(message: 'Message'):
#             message.set_body_codec(body_codec)
#
#         return decorated_body_codec
#
#     @staticmethod
#     def with_body(body: 'Any'):
#         def decorated_body(message: 'Message'):
#             message.set_body_codec(body)
#
#         return decorated_body
#
#     @staticmethod
#     def with_xfer_pipe(filter_id: 'Iterator'):
#         def decorated_xfer_pipe(message: 'Message'):
#             message.xfer_pipe.append(filter_id)
#
#         return decorated_xfer_pipe
