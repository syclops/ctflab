Instructions for this problem
-----------------------------

For this problem, you need to implement a bitwise XOR function in C.

However, there are a few restrictions. You can only use these operators:

~ &

And you can only use this many operators total:

14

You cannot use other operators, function calls, conditionals, or loops. You are
allowed to use constants, but they must be between 0 and 255.

Testing your solution and getting the flag
------------------------------------------

You can test your solution by running ./run_tests, which reads your
implementation (i.e., the body of your function) from standard input. So your
input might look something like

return x & y;

(Obviously that's not the correct solution.)

Once you have entered this, the script will do two things. First, it will
perform a syntax check to ensure that your implementation meets the syntax
constraints above. Second, it will run a set of test cases to ensure that your
implementation is correct. Some of these test cases will be randomly generated,
so you will get different tests each time you run this.

If any part of the script fails, it will exit immediately, so if you fail the
syntax check, the script will not do any correctness checks. If all checks
succeed, the script prints out the flag.
