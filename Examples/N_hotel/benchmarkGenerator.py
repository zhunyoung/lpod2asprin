# 1. This python code generates the programs for benchmark N_hotel given the value of n

# 2. For the same LPOD, there will be two programs generated, 
#    one in the path ./lpod2asprin/ is the input program to lpod2asprin
#    another in the path ./lpod/ is the input program to the original implementation of LPOD

# 3. Example Command Line:
#    python benchmarkGenerator.py -n 3

import sys, getopt, random, os

def main(argv):
   n = '3'
   lpod2asprin_input = "default.txt"
   lpod_input = "default.txt"
   try:
      opts, args = getopt.getopt(argv,"h:n:",["n="])
   except getopt.GetoptError:
      print("python benchmarkGenerator.py -n <number> ")
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print("python benchmarkGenerator.py -n <number> ")
         sys.exit()
      elif opt in ("-n", "--n"):
         n = arg

   
   if not os.path.exists("lpod2asprin"):
    os.makedirs("lpod2asprin")

   if not os.path.exists("lpod"):
    os.makedirs("lpod")

   lpod2asprin_input = "lpod2asprin/" + n + ".txt"
   lpod_input = "lpod/" + n + ".txt"

   print("n is " + n)
   print("the input to lpod2asprin is " + lpod2asprin_input)
   print("the input to the original lpod system is " + lpod_input)

   

   hotel_benchmark = '''% We need to choose a hotel from n hotels. We randomly assign the order of their price, distance, and service.

1{hotel(X): dom(X)}1.

price(X) :- hotel(X), dom(X).
distance(X) :- hotel(X), dom(X).
service(X) :- hotel(X), dom(X).

:- hotel(X), price(Y), X!=Y, dom(X), dom(Y).
:- hotel(X), distance(Y), X!=Y, dom(X), dom(Y).
:- hotel(X), service(Y), X!=Y, dom(X), dom(Y).

'''


   # we randonly assign the order for all hotels for each input language
   price_lpod2asprin = ""
   distance_lpod2asprin = ""
   service_lpod2asprin = ""

   price_lpod = ""
   distance_lpod = ""
   service_lpod = ""

   prices = []
   for i in range(int(n)):
        prices.append("price("+str(i+1) + ")")

   random.shuffle(prices)
   for i in prices:
        price_lpod2asprin += (" >> " + i)
        price_lpod += (" x " + i)

   distances = []
   for i in range(int(n)):
        distances.append("distance("+str(i+1) + ")")

   random.shuffle(distances)
   for i in distances:
        distance_lpod2asprin += (" >> " + i)
        distance_lpod += (" x " + i)

   services = []
   for i in range(int(n)):
        services.append("service("+str(i+1) + ")")

   random.shuffle(services)
   for i in services:
        service_lpod2asprin += (" >> " + i)
        service_lpod += (" x " + i)


   hotel_benchmark_lpod2asprin = hotel_benchmark + "dom(1.." + n + ").\n\n" + price_lpod2asprin[4:] + ".\n" + distance_lpod2asprin[4:] + ".\n" + service_lpod2asprin[4:] + ".\n"

   hotel_benchmark_lpod = hotel_benchmark + "dom(1.." + n + ").\n\n" + price_lpod[3:] + ".\n" + distance_lpod[3:] + ".\n" + service_lpod[3:] + ".\n"

   with open (lpod2asprin_input,'w') as fw:
   	  fw.write(hotel_benchmark_lpod2asprin)
   with open (lpod_input,'w') as fw:
        fw.write(hotel_benchmark_lpod)


if __name__ == "__main__":
   main(sys.argv[1:])