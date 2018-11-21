% facts
male('Prince Phillip').
male('Prince Charles').
male('Captain Mark Phillips').
male('Timothy Laurence').
male('Prince Andrew').
male('Prince Edward').
male('Prince William').
male('Prince Harry').
male('Peter Phillips').
male('Mike Tindall').
male('James Viscount Severn').
male('Prince Geogre').

female('Queen Elizabeth II').
female('Princess Diana').
female('Camilla Parker Bowles').
female('Princess Anne').
female('Sarah Ferguson').
female('Sophie Rhys Jones').
female('Kate Middleton').
female('Autumn Kelly').
female('Zara Phillips').
female('Princess Beatrice').
female('Princess Eugenie').
female('Lady Louise Mountbatten Windsor').
female('Princess Charlotte').
female('Savannah Phillips').
female('Isla Phillips').
female('Mia Grace Tindall').

married('Queen Elizabeth II', 'Prince Phillip').
married('Prince Charles', 'Camilla Parker Bowles').
married('Prince William', 'Kate Middleton').
married('Princess Anne', 'Timothy Laurence').
married('Autumn Kelly', 'Peter Phillips').
married('Zara Phillips', 'Mike Tindall').
married('Sophie Rhys Jones', 'Prince Edward').

married('Prince Phillip', 'Queen Elizabeth II').
married('Camilla Parker Bowles', 'Prince Charles').
married('Kate Middleton', 'Prince William').
married('Timothy Laurence', 'Princess Anne').
married('Peter Phillips', 'Autumn Kelly').
married('Mike Tindall', 'Zara Phillips').
married('Prince Edward', 'Sophie Rhys Jones').

divorced('Princess Diana', 'Prince Charles').
divorced('Captain Mark Phillips', 'Princess Anne').
divorced('Sarah Ferguson', 'Prince Andrew').

divorced('Prince Charles', 'Princess Diana').
divorced('Princess Anne', 'Captain Mark Phillips').
divorced('Prince Andrew', 'Sarah Ferguson').

% row 0 and 1
parent('Queen Elizabeth II', 'Prince Charles').
parent('Queen Elizabeth II', 'Princess Anne').
parent('Queen Elizabeth II', 'Prince Andrew').
parent('Queen Elizabeth II', 'Prince Edward').
parent('Prince Phillip', 'Prince Charles').
parent('Prince Phillip', 'Princess Anne').
parent('Prince Phillip', 'Prince Andrew').
parent('Prince Phillip', 'Prince Edward').

% row 1 and 2
parent('Princess Diana', 'Prince William').
parent('Princess Diana', 'Prince Harry').
parent('Prince Charles', 'Prince William').
parent('Prince Charles', 'Prince Harry').

parent('Captain Mark Phillips', 'Peter Phillips').
parent('Captain Mark Phillips', 'Zara Phillips').
parent('Princess Anne', 'Peter Phillips').
parent('Princess Anne', 'Zara Phillips').

parent('Sarah Ferguson', 'Princess Beatrice').
parent('Sarah Ferguson', 'Princess Eugenie').
parent('Prince Andrew', 'Princess Beatrice').
parent('Prince Andrew', 'Princess Eugenie').

parent('Sophie Rhys Jones', 'James Viscount Severn').
parent('Sophie Rhys Jones', 'Lady Louise Mountbatten Windsor').
parent('Prince Edward', 'James Viscount Severn').
parent('Prince Edward', 'Lady Louise Mountbatten Windsor').

% row 2 and 3
parent('Prince William', 'Prince Geogre').
parent('Prince William', 'Princess Charlotte').
parent('Kate Middleton', 'Prince Geogre').
parent('Kate Middleton', 'Princess Charlotte').

parent('Autumn Kelly', 'Savannah Phillips').
parent('Autumn Kelly', 'Isla Phillips').
parent('Peter Phillips', 'Savannah Phillips').
parent('Peter Phillips', 'Isla Phillips').

parent('Zara Phillips', 'Mia Grace Tindall').
parent('Mike Tindall', 'Mia Grace Tindall').

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
	parent(X, NieceNephew),	sister(Person, X) ; 
	uncle(Y, NieceNephew), wife(Person, Y).

uncle(Person, NieceNephew) :-
	parent(X, NieceNephew),	brother(Person, X):
	aunt(Y, NieceNephew), husband(Person, Y).

niece(Person, AuntUncle) :-
	aunt(AuntUncle, Person),
	female(Person).

nephew(Person, AuntUncle) :-
	uncle(AuntUncle, Person),
	male(Person).