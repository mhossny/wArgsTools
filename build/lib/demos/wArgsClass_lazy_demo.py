from wArgs import wArgsClass, wArgsChk, wArgsInit

class Person():
    '''
    This class specifies peersonal details.
    '''
    def __init__(self, name='No Name', age=-1, height=-1., weight=-1.):
        self.__dict__.update(locals())
        pass

class Student(Person):
    '''
    This class dictates each student to havee an `id`.
    Personal details are inherited from `Peerson`.
    '''
    def __init__(self, id, score=None, **kwargs):
        Person.__init__(self, **kwargs)
        self.__dict__.update(locals())
        pass

    def print(self):
        print(f'ID:\t{self.id}')
        print(f'Name:\t{self.name}')
        print(f'Age:\t{self.age}')
        print(f'Height:\t{self.height}')
        print(f'Weight:\t{self.weight}')
        print(f'Score:\t{self.score}')
        print()
                
    def __repr__(self): return self.__dict__.__repr__()

wArgsInit(globals())
    
# Lazy Call
wArgsPersonC = wArgsClass(Person, parse_pos_args=True)
wArgsStudentC = wArgsClass(Student, parse_pos_args=True)
wArgsChk()

student = wArgsStudentC()
student.print()
