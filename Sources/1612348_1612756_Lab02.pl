% facts
male(prince_phillip).
male(prince_charles).
male(captain_mark_phillips).
male(timothy_laurence).
male(prince_andrew).
male(prince_edward).
male(prince_william).
male(prince_harry).
male(peter_phillips).
male(mike_tindall).
male(james_viscount_severn).
male(prince_geogre).

female(queen_elizabeth_ii).
female(princess_diana).
female(camilla_parker_bowles).
female(princess_anne).
female(sarah_ferguson).
female(sophie_rhys_jones).
female(kate_middleton).
female(autumn_kelly).
female(zara_phillips).
female(princess_beatrice).
female(princess_eugenie).
female(lady_louise_mountbatten_windsor).
female(princess_charlotte).
female(savannah_phillips).
female(isla_phillips).
female(mia_grace_tindall).

married(queen_elizabeth_ii, prince_phillip).
married(prince_charles, camilla_parker_bowles).
married(prince_william, kate_middleton).
married(princess_anne, timothy_laurence).
married(autumn_kelly, peter_phillips).
married(zara_phillips, mike_tindall).
married(sophie_rhys_jones, prince_edward).

married(prince_phillip, queen_elizabeth_ii).
married(camilla_parker_bowles, prince_charles).
married(kate_middleton, prince_william).
married(timothy_laurence, princess_anne).
married(peter_phillips, autumn_kelly).
married(mike_tindall, zara_phillips).
married(prince_edward, sophie_rhys_jones).

divorced(princess_diana, prince_charles).
divorced(captain_mark_phillips, princess_anne).
divorced(sarah_ferguson, prince_andrew).

divorced(prince_charles, princess_diana).
divorced(princess_anne, captain_mark_phillips).
divorced(prince_andrew, sarah_ferguson).

% row 0 and 1
parent(queen_elizabeth_ii, prince_charles).
parent(queen_elizabeth_ii, princess_anne).
parent(queen_elizabeth_ii, prince_andrew).
parent(queen_elizabeth_ii, prince_edward).
parent(prince_phillip, prince_charles).
parent(prince_phillip, princess_anne).
parent(prince_phillip, prince_andrew).
parent(prince_phillip, prince_edward).

% row 1 and 2
parent(princess_diana, prince_william).
parent(princess_diana, prince_harry).
parent(prince_charles, prince_william).
parent(prince_charles, prince_harry).

parent(captain_mark_phillips, peter_phillips).
parent(captain_mark_phillips, zara_phillips).
parent(princess_anne, peter_phillips).
parent(princess_anne, zara_phillips).

parent(sarah_ferguson, princess_beatrice).
parent(sarah_ferguson, princess_eugenie).
parent(prince_andrew, princess_beatrice).
parent(prince_andrew, princess_eugenie).

parent(sophie_rhys_jones, james_viscount_severn).
parent(sophie_rhys_jones, lady_louise_mountbatten_windsor).
parent(prince_edward, james_viscount_severn).
parent(prince_edward, lady_louise_mountbatten_windsor).

% row 2 and 3
parent(prince_william, prince_geogre).
parent(prince_william, princess_charlotte).
parent(kate_middleton, prince_geogre).
parent(kate_middleton, princess_charlotte).

parent(autumn_kelly, savannah_phillips).
parent(autumn_kelly, isla_phillips).
parent(peter_phillips, savannah_phillips).
parent(peter_phillips, isla_phillips).

parent(zara_phillips, mia_grace_tindall).
parent(mike_tindall, mia_grace_tindall).

% rules
husband(Person, Wife) :-
	married(Person, Wife),
	married(Wife, Person),
	male(Person).
	
wife(Person, Husband) :-
	married(Person, Husband),
	married(Husband, Person),
	female(Person).
	
father(Parent, Child) :-
	parent(Parent, Child),
	male(Parent).
	
mother(Parent, Child) :-
	parent(Parent, Child),
	female(Parent).
	
child(Child, Parent) :-
	parent(Parent, Child).
	
son(Child, Parent) :-
	child(Child, Parent),
	male(Child).
	
daughter(Child, Parent) :-
	child(Child, Parent),
	female(Child).


grandparent(GP, GC) :-
	parent(GP, X),
	parent(X, GC).

grandmother(GM, GC) :-
	grandparent(GM, GC),
	female(GM).

grandfather(GF, GC) :-
	grandparent(GF, GC),
	male(GF).

grandchild(GC, GP) :-
	grandparent(GP, GC).

grandson(GS, GP) :-
	grandchild(GS, GP),
	male(GS).

granddaughter(GD, GP) :-
	grandchild(GD, GP),
	female(GD).

sibling(Person1, Person2) :-
	parent(X, Person1),
	parent(X, Person2).

brother(Person, Sibling) :-
	sibling(Person, Sibling),
	male(Person).

sister(Person, Sibling) :-
	sibling(Person, Sibling),
	female(Person).

aunt(Person, NieceNephew) :-
	parent(X, NieceNephew),
	sister(Person, X).

uncle(Person, NieceNephew) :-
	parent(X, NieceNephew),
	brother(Person, X).

niece(Person, AuntUncle) :-
	aunt(AuntUncle, Person),
	female(Person).

nephew(Person, AuntUncle) :-
	uncle(AuntUncle, Person),
	male(Person).
	


