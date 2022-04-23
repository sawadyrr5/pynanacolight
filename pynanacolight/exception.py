class PyNanacoException(Exception):
    """エラー基底クラス"""


class InvalidGiftIDException(PyNanacoException):
    """ギフトコード無効エラー"""


class GiftIDAlreadyRegisteredException(PyNanacoException):
    """ギフトコード無効エラー"""
