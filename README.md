# lpod2asprin
An LPOD solver based on asprin

## Homepage
http://reasoning.eas.asu.edu/lpod2asprin/

## Prerequisite
The `lpod2asprin` system requires the installation of [`asprin`](https://github.com/potassco/asprin) and [ply](https://github.com/dabeaz/ply). You can install `asprin` via
```
pip install asprin
```
and ply via
```
pip install ply
```

You can test if `asprin` is installed successfully via 
```
asprin --test
```

## Installation
Clone this repo:
```
git clone https://github.com/zhunyoung/lpod2asprin
cd lpod2asprin
```

## Usage
There are 4 preference criteria for LPOD: cardinality `c`, inclusion `i`, Pareto `p`, and penalty-sum `ps`. You can find the k-preferred (k is one of {c, i, p, ps}) answer set of an LPOD stored in file `input.txt` by executing
```
python lpod2asprin.py -i input.txt -type k
```

## Example
To find the ps-preferred answer set of the hotel example, you can execute
```
python lpod2asprin.py -i Examples/hotel.txt -type ps
```
which will output
```
Input LPOD program: Examples/hotel.txt
Type of LPOD preference criterion: ps

asprin version 3.0.2
Reading from /Users/young/Desktop/test/lpod2asprin/lpod.lp ...
Solving...
Answer: 1
dom(1) dom(2) dom(3) hotel(3) tooFar star4
Answer: 2
dom(1) dom(2) dom(3) hotel(2) med star3
OPTIMUM FOUND
Answer: 3
dom(1) dom(2) dom(3) hotel(1) close star2
OPTIMUM FOUND

Models       : 3
  Optimum    : yes
  Optimal    : 2
```
