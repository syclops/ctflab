from hacksport.problem import Challenge, File

class Problem(Challenge):

    def generate_flag(self, _):
        return "zero_wing_cats"

    def setup(self):
        pass

    def initialize(self):
        self.files = [File('allyourbase64.png')]
