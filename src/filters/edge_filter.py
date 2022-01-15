# custom data structure to hold the state of a Canny edge filter
class EdgeFilter:

    def __init__(self, kernelSize=None, erodeIter=None, dilateIter=None, canny1=None,
                 canny2=None, hasEdge=False):
        self.kernelSize = kernelSize
        self.erodeIter = erodeIter
        self.dilateIter = dilateIter
        self.canny1 = canny1
        self.canny2 = canny2
        self.hasEdge = hasEdge

    def to_data(self):
        return {
            "kernelSize": self.kernelSize,
            "erodeIter": self.erodeIter,
            "dilateIter": self.dilateIter,
            "canny1": self.canny1,
            "canny2": self.canny2,
            "hasEdge": self.hasEdge,
        }

    @staticmethod
    def from_data(json):
        edge_filter = EdgeFilter()

        if "kernelSize" in json:
            edge_filter.kernelSize = json["kernelSize"]
        if "erodeIter" in json:
            edge_filter.erodeIter = json["erodeIter"]
        if "dilateIter" in json:
            edge_filter.dilateIter = json["dilateIter"]
        if "canny1" in json:
            edge_filter.canny1 = json["canny1"]
        if "canny2" in json:
            edge_filter.canny2 = json["canny2"]
        if "hasEdge" in json:
            edge_filter.hasEdge = json["hasEdge"]

        return edge_filter
