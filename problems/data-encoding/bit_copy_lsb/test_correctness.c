/**
 *
 */

#include <stdio.h>
#include <stdlib.h>

#include "bit_copy_lsb.h"

/**
 * Print information about a failed test case to standard error.
 *
 * @param x The left operand for the test function.
 * @param expected_result The expected result.
 * @param actual_result The actual result.
 */
void print_error(int x, int expected_result, int actual_result)
{
  fprintf(stderr, "bit_copy_lsb(%d) failed (expected %d, got %d)\n", x,
          expected_result, actual_result);
}

/**
 * Return the expected result of the function.
 */
int compute_function(int x)
{
  return (x & 1) ? -1 : 0;
}

/**
 * Run a single test case.
 *
 * @param x The left operand for the test function.
 * @param n The right operand for the test function.
 * @return 1 if the function produces the expected result and 0 otherwise.
 */
int test_case(int x)
{
  int expected_result = compute_function(x);
  int test_result = bit_copy_lsb(x);
  if (expected_result != test_result) {
    print_error(x, expected_result, test_result);
  }
  return expected_result == bit_copy_lsb(x);
}

/**
 * Run a set of standard tests.
 *
 * @return 1 if all test cases pass and 0 otherwise.
 */
int standard_tests()
{
  if (!test_case(0)) {
    return 0;
  }
  if (!test_case(1)) {
    return 0;
  }
  if (!test_case(-1)) {
    return 0;
  }
  return 1;
}

/**
 * Randomly generate and run test cases.
 *
 * @param num_tests The number of random test cases to generate and run.
 * @return 1 if all test cases pass and 0 otherwise.
 */
int randomized_tests(int num_tests)
{
  int x;
  for (int i = 0; i < num_tests; ++i) {
    x = rand();
    if (!test_case(x)) {
      return 0;
    }
  }
  return 1;
}

void usage(char* program_name)
{
  fprintf(stderr, "Usage: %s <num_random_tests>\n", program_name);
}

int main(int argc, char* argv[]) {
  if (argc != 2) {
    usage(argv[0]);
    exit(EXIT_FAILURE);
  }
  if (!standard_tests()) {
    fprintf(stderr, "Correctness test failed, exiting\n");
    exit(EXIT_FAILURE);
  }
  int num_tests = atoi(argv[1]);
  if (num_tests < 1) {
    fprintf(stderr, "Number of randomized tests must be positive.\n");
    exit(EXIT_FAILURE);
  }
  if (!randomized_tests(num_tests)) {
    fprintf(stderr, "Correctness test failed, exiting\n");
    exit(EXIT_FAILURE);
  }
  fprintf(stderr, "Correctness tests succeeded\n");
  return EXIT_SUCCESS;
}
