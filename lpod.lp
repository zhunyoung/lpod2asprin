#program preference(lpod(c)).

degree(R,1) :- preference(S, lpod(_)),
	preference(S,R,1,for(A),_), holds(A).
degree(R,D-1) :- preference(S, lpod(_)),
	preference(S,R,D,for(A),_), holds(A), D>1,
	not holds(B): preference(S,R,J,for(B),_), 0<J, J<D.

degree'(R,1) :- preference(S, lpod(_)),
	preference(S,R,1,for(A),_), holds'(A).
degree'(R,D-1) :- preference(S, lpod(_)),
	preference(S,R,D,for(A),_), holds'(A), D>1,
	not holds'(B): preference(S,R,J,for(B),_), 0<J, J<D.

worse2degree(S,D) :- optimize(S), preference(S,lpod(c)),
	degree'(_,D),
	#sum{ 1,R: degree'(R,D);
	     -1,R: degree(R,D)} > 0.

better(S) :- optimize(S), preference(S,lpod(c)),
	degree(_,D),
	#sum{ 1,R: degree(R,D);
	     -1,R: degree'(R,D)} > 0,
	not worse2degree(S,J) : J=1..D-1.




#program preference(lpod(i)).

degree(R,1) :- preference(S, lpod(_)),
	preference(S,R,1,for(A),_), holds(A).
degree(R,D-1) :- preference(S, lpod(_)),
	preference(S,R,D,for(A),_), holds(A), D>1,
	not holds(B): preference(S,R,J,for(B),_), 0<J, J<D.

degree'(R,1) :- preference(S, lpod(_)),
	preference(S,R,1,for(A),_), holds'(A).
degree'(R,D-1) :- preference(S, lpod(_)),
	preference(S,R,D,for(A),_), holds'(A), D>1,
	not holds'(B): preference(S,R,J,for(B),_), 0<J, J<D.

prf2degree(S,D) :- preference(S,lpod(i)),
	degree(_,D), 
	#count{J: degree(J,D), not degree'(J,D)} > 0,
	degree(J,D):degree'(J,D).

better(S) :- preference(S,lpod(i)),
	prf2degree(S,D), 
	degree(R,J):degree'(R,J), J<D.


#program preference(lpod(p)).

degree(R,1) :- preference(S, lpod(_)),
	preference(S,R,1,for(A),_), holds(A).
degree(R,D-1) :- preference(S, lpod(_)),
	preference(S,R,D,for(A),_), holds(A), D>1,
	not holds(B): preference(S,R,J,for(B),_), 0<J, J<D.

degree'(R,1) :- preference(S, lpod(_)),
	preference(S,R,1,for(A),_), holds'(A).
degree'(R,D-1) :- preference(S, lpod(_)),
	preference(S,R,D,for(A),_), holds'(A), D>1,
	not holds'(B): preference(S,R,J,for(B),_), 0<J, J<D.

equ(S) :- preference(S,lpod(p)),
	D1=D2: degree(R,D1), degree'(R,D2).


better(S) :- preference(S,lpod(p)),
	not equ(S),
	D1<=D2 : degree(R,D1),degree'(R,D2).

#program preference(lpod(ps)).

degree(R,1) :- preference(S, lpod(_)),
	preference(S,R,1,for(A),_), holds(A).
degree(R,D-1) :- preference(S, lpod(_)),
	preference(S,R,D,for(A),_), holds(A), D>1,
	not holds(B): preference(S,R,J,for(B),_), 0<J, J<D.

degree'(R,1) :- preference(S, lpod(_)),
	preference(S,R,1,for(A),_), holds'(A).
degree'(R,D-1) :- preference(S, lpod(_)),
	preference(S,R,D,for(A),_), holds'(A), D>1,
	not holds'(B): preference(S,R,J,for(B),_), 0<J, J<D.

better(S) :- preference(S,lpod(ps)),
	#sum{D,R : degree(R,D); 
	    -D,R : degree'(R,D)} < 0.