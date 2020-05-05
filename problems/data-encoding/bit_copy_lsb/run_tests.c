/**
 * Print the contents of a flag file if user input passes all checks.
 *
 * Author: Steve Matsumoto <stephanos.matsumoto@sporic.me>
 */
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#define CAT "/bin/cat"
#define SED "/bin/sed"
#define GCC "/usr/bin/gcc"
#define PYTHON "/usr/bin/python3"
#define BODY "body.txt"
#define FUNCTION "bit_copy_lsb"
#define HEADER FUNCTION ".h"
#define TEMPLATE FUNCTION "_template.h"
#define PREPROCESSED FUNCTION ".i"
#define CHECK_CORRECTNESS "test_correctness"
#define CHECK_CORRECTNESS_SRC CHECK_CORRECTNESS ".c"
#define FLAG "flag.txt"
#define CHECK_SYNTAX "test_syntax.py"
#define ALLOWED_OPS "!,~,&,^,|,+,<<,>>"
#define MAX_OPS "5"
#define NUM_RANDOM_TESTS "10000"

void cleanup()
{
  system("rm -f " BODY);
  system("rm -f " PREPROCESSED);
  system("rm -f " CHECK_CORRECTNESS);
  system("cp " TEMPLATE " " HEADER);
  system("chmod 777 " HEADER);
}

/**
 * Print an error message and exit with a failure code.
 *
 * @param error_message An error message ending with a newline and null char.
 */
void error_and_exit(char* error_message)
{
  fputs(error_message, stderr);
  cleanup();
  exit(EXIT_FAILURE);
}

/**
 * Execute a command, and exit with an error message if unsuccessful.
 *
 * @param args A null-terminated array of arguments to pass to exec.
 * @param input_file The input file path (defaults to stdin).
 * @param output_file The output file path (defaults to stdout).
 */
void run_command(char* args[], char* input_file, char* output_file)
{
  pid_t process_id = fork();

  if (process_id == 0) {
    if (input_file && freopen(input_file, "r", stdin) == NULL) {
      error_and_exit("freopen failed for input file\n");
    }
    if (output_file && freopen(output_file, "w", stdout) == NULL) {
      error_and_exit("freopen failed for output file\n");
    }
    execv(args[0], args);
  } else if (process_id > 0) {
    int exit_status;
    wait(&exit_status);
    if (!WIFEXITED(exit_status)) {
      error_and_exit("Command did not terminate normally\n");
    } else if (WEXITSTATUS(exit_status)) {
      error_and_exit("Command exited with non-zero code\n");
    }
  } else {
    fprintf(stderr, "[error] Failed to fork process, aborting\n");
    exit(EXIT_FAILURE);
  }
}

int main(void)
{
  puts("Input the function body below (Enter, then Ctrl-D when done):");
  run_command((char*[]) {CAT, NULL}, NULL, BODY);
  run_command((char*[]) {SED, "-i",
                         "s/\\/\\/ INPUT GOES HERE/cat " BODY "/e",
                         HEADER, NULL}, NULL, NULL);
  run_command((char*[]) {GCC, "-E", HEADER, "-o", PREPROCESSED, NULL}, NULL,
              NULL);
  run_command((char*[]) {PYTHON, CHECK_SYNTAX, FUNCTION, ALLOWED_OPS, MAX_OPS,
                         NULL}, PREPROCESSED, NULL);
  run_command((char*[]) {GCC, "-O3", "-o", CHECK_CORRECTNESS,
                         CHECK_CORRECTNESS_SRC, NULL}, NULL, NULL);
  run_command((char*[]) {"./" CHECK_CORRECTNESS, NUM_RANDOM_TESTS, NULL}, NULL,
              NULL);
  puts("All tests passed! Here's the flag:");
  run_command((char*[]) {CAT, FLAG, NULL}, NULL, NULL);
  cleanup();
  return 0;
}
