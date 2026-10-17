class Shape: 

    def area(self):
        return 0 


class Circle(Shape):
    def __init__(self, radius): 
        self.radius = radius 

    def area(self): 
        return 3.14159 * self.radius ** 2 
        

class Rectangle(Shape): 

    def __init__(self, w, h): 
        self.w = w; self.h = h 
    
    def area(self): 
        return self.w * self.h 

# Same call — different behaviour (polymorphism) 
shapes = [Circle(5), Rectangle(4, 6)] 
for shape in shapes: 
    print(shape.area()) # 78.53... then 24 
