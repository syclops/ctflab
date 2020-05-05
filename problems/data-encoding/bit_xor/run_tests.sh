#!/usr/bin/env bash

set -o errexit

function cleanup {
  rm -f body.txt
  rm -f test_correctness
  cp bit_xor_template.h bit_xor.h
  chmod 777 bit_xor.h
}
trap cleanup EXIT

echo "Input the body of the function below (Enter, then Ctrl-D when done):"
cat > body.txt
sed -i 's/\/\/ INPUT GOES HERE/cat body.txt/e' bit_xor.h
gcc -E bit_xor.h | python3 test_syntax.py bit_xor '~,&' 14
gcc -O3 -o test_correctness test_correctness.c
./test_correctness 1000
echo "All tests passed!"
