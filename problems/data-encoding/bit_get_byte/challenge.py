from hacksport.problem import Challenge, File

class Problem(Challenge):

    def generate_flag(self, _):
        with open("flag.txt", "r") as f:
            flag = f.read().strip().split('{')[1][:-1]
        return flag

    def setup(self):
        pass

    def initialize(self):
        self.files = [
            File("bit_get_byte.h", permissions=0o755),
            File("bit_get_byte_template.h", permissions=0o755),
            File("flag.txt", permissions=0o500),
            File("README.txt", permissions=0o644),
            File("run_tests", permissions=0o4755, user='root'),
            File("test_correctness.c", permissions=0o755),
            File("test_syntax.py", permissions=0o755),
        ]
