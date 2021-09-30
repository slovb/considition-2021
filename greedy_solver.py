import operator


class GreedySolver:
    xp = 0
    zp = 0
    yp = 0
    heavyPackages = []
    otherPackages = []
    placedPackages = []
    lastKnownMaxWidth = 0
    lastKnownMaxLength = 0
    lastKnownMaxHeight = 0

    def __init__(self, game_info):
        self.vehicle_length = game_info["vehicle"]["length"]
        self.vehicle_width = game_info["vehicle"]["width"]
        self.vehicle_height = game_info["vehicle"]["height"]
        self.packages = game_info["dimensions"]
        for package in self.packages:
            if(package["height"] and package["weightClass"] == 2 > self.lastKnownMaxHeight):
                self.lastKnownMaxHeight = package["height"]
            if(package["weightClass"] == 2):
                self.heavyPackages.append(
                    {"area": package["width"]*package["length"], "id": package["id"]})
            elif(package["weightClass"] != 2):
                self.otherPackages.append(
                    {"area": package["width"]*package["length"], "id": package["id"]})
        self.heavyPackages = sorted(
            self.heavyPackages, key=lambda i: (i['area']))
        self.otherPackages = sorted(
            self.otherPackages, key=lambda i: (i['area']))

    def Solve(self):
        for p in self.packages:
            if(self.zp <= self.lastKnownMaxHeight):
                id = self.heavyPackages.pop()["id"]
                package = self.packages[id]
            elif(len(self.otherPackages) != 0):
                id = self.otherPackages.pop()["id"]
                package = self.packages[id]
            else:
                id = self.heavyPackages.pop()["id"]
                package = self.packages[id]

            if(self.DoesPackageFitZ(package)):
                self.AddPackage(package)
                self.zp += package["height"]

            elif(self.DoesPackageFitY(package)):
                self.yp += self.lastKnownMaxWidth
                self.zp = 0
                self.AddPackage(package)
                self.zp = package["height"]
                self.lastKnownMaxWidth = 0

            elif(self.DoesPackageFitX(package)):
                self.xp += self.lastKnownMaxLength
                self.yp = 0
                self.zp = 0
                self.AddPackage(package)
                self.zp = package["height"]
                self.lastKnownMaxLength = 0

            else:
                print("Something went terribly wrong!")
                break
            self.SetMaxX(package)
            self.SetMaxY(package)
        return self.placedPackages

    def DoesPackageFitX(self, package):
        return self.xp + self.lastKnownMaxLength + package["length"] < self.vehicle_length

    def DoesPackageFitY(self, package):
        return self.yp + self.lastKnownMaxWidth + package["width"] < self.vehicle_width and self.xp + package["length"] < self.vehicle_length

    def DoesPackageFitZ(self, package):
        return self.xp + package["length"] < self.vehicle_length and self.yp + package["width"] < self.vehicle_width and self.zp + package["height"] < self.vehicle_height

    def SetMaxY(self, package):
        if(package["width"] > self.lastKnownMaxWidth):
            self.lastKnownMaxWidth = package["width"]

    def SetMaxX(self, package):
        if(package["length"] > self.lastKnownMaxLength):
            self.lastKnownMaxLength = package["length"]

    def AddPackage(self, package):
        self.placedPackages.append({"id": package["id"], "x1": self.xp, "x2": self.xp, "x3": self.xp, "x4": self.xp,
                                    "x5": self.xp + package["length"], "x6": self.xp + package["length"], "x7": self.xp + package["length"], "x8": self.xp + package["length"],
                                    "y1": self.yp, "y2": self.yp, "y3": self.yp, "y4": self.yp,
                                    "y5": self.yp + package["width"], "y6": self.yp + package["width"], "y7": self.yp + package["width"], "y8": self.yp + package["width"],
                                    "z1": self.zp, "z2": self.zp, "z3": self.zp, "z4": self.zp,
                                    "z5": self.zp + package["height"], "z6": self.zp + package["height"], "z7": self.zp + package["height"], "z8": self.zp + package["height"], "weightClass": package["weightClass"], "orderClass": package["orderClass"]})