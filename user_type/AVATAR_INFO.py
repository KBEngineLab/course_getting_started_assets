class AvatarInfo(dict):
    """
    """
    def __init__(self):
        """
        """
        dict.__init__(self)

    def asDict(self):
        data = {
            "dbid": self["dbid"],
            "name": self["name"],
        }
        return data

    def createFromDict(self, dictData):
        self["dbid"] = dictData["dbid"]
        self["name"] = dictData["name"]
        return self

class AVATAR_INFO_PICKLER:
    def __init__(self):
        pass

    def createObjFromDict(self, dict):
        return AvatarInfo().createFromDict(dict)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, AvatarInfo)


avatar_info_inst = AVATAR_INFO_PICKLER()