class Circle:

    def __init__(self,centre,radius):
        self.centre = centre
        self.radius = radius

    def __contains__(self,other):
        x = self.centre[0]-other[0]
        y = self.centre[1]-other[1]
        dis = (x**2+y**2)**(0.5)
        if dis < self.radius:
            return True
        else:
            return False