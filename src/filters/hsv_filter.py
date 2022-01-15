# custom data structure to hold the state of an HSV filter
class HsvFilter:

    def __init__(self, hMin=0, sMin=0, vMin=0, hMax=179, sMax=255, vMax=255,
                 sAdd=0, sSub=0, vAdd=0, vSub=0):
        self.hMin = hMin
        self.sMin = sMin
        self.vMin = vMin
        self.hMax = hMax
        self.sMax = sMax
        self.vMax = vMax
        self.sAdd = sAdd
        self.sSub = sSub
        self.vAdd = vAdd
        self.vSub = vSub

    def to_data(self):
        return {
            "hMin": self.hMin,
            "sMin": self.sMin,
            "vMin": self.vMin,
            "hMax": self.hMax,
            "sMax": self.sMax,
            "vMax": self.vMax,
            "sAdd": self.sAdd,
            "sSub": self.sSub,
            "vAdd": self.vAdd,
            "vSub": self.vSub,
        }

    @staticmethod
    def from_data(json):
        hsv_filter = HsvFilter()

        if "hMin" in json:
            hsv_filter.hMin = json["hMin"]
        if "sMin" in json:
            hsv_filter.sMin = json["sMin"]
        if "vMin" in json:
            hsv_filter.vMin = json["vMin"]
        if "hMax" in json:
            hsv_filter.hMax = json["hMax"]
        if "sMax" in json:
            hsv_filter.sMax = json["sMax"]
        if "vMax" in json:
            hsv_filter.vMax = json["vMax"]
        if "sAdd" in json:
            hsv_filter.sAdd = json["sAdd"]
        if "sSub" in json:
            hsv_filter.sSub = json["sSub"]
        if "vAdd" in json:
            hsv_filter.vAdd = json["vAdd"]
        if "vSub" in json:
            hsv_filter.vSub = json["vSub"]

        return hsv_filter
