classification('Corn','Plants').
classification('Flower','Plants').
classification('Lavenders','Plants').
classification('Mangoes','Plants').
classification('Grass','Plants').
classification('Acorns','Plants').
classification('Grasshopper','Insects').
classification('Butterfly','Insects').
classification('Fruit fly','Insects').
classification('Deer','Mammals').
classification('Squirrel','Mammals').
classification('Rabbit','Mammals').
classification('Rat','Mammals').
classification('Frog','Amphibians').
classification('Dragonfly','Insects').
classification('Thrush','Birds').
classification('Fox','Mammals').
classification('Coyote','Mammals').
classification('Python','Reptiles').
classification('Wolf','Mammals').
classification('Eagle','Birds').
classification('Chicken','Birds').


eat('Corn','Grasshopper').
eat('Flower','Butter fly').
eat('Lavenders','Butter fly').
eat('Mangoes','Fruit fly').
eat('Grass','Deer').
eat('Acorns','Squirrel').
eat('Grass','Rabbit').

eat('Grasshopper','Rat').
eat('Grasshopper','Frog').
eat('Butter fly','Frog').
eat('Butter fly','Dragonfly').
eat('Fruit fly','Dragonfly').
eat('Fruit fly','Frog').
eat('Fruit fly','Thrush').
eat('Dragonfly','Frog').
eat('Dragonfly','Thrush').
eat('Deer','Fox').
eat('Deer','Coyote').
eat('Squirrel','Fox').
eat('Squirrel','Coyote').
eat('Rabbit','Fox').
eat('Rabbit','Coyote').
eat('Rabbit','Eagle').

eat('Corn','Chicken').
eat('Grasshopper','Chicken').
eat('Chicken','Eagle').
eat('Chicken','Fox').
eat('Chicken','Coyote').

eat('Rat','Python').
eat('Rat','Eagle').
eat('Rat','Wolf').
eat('Frog','Python').
eat('Frog','Eagle').
eat('Thrush','Wolf').
eat('Thrush','Eagle').

eat('Wolf','Python').
eat('Wolf','Eagle').

eat('Python','Eagle').

beEaten(X,Y):- eat(Y,X).

%Loai dong vat an thuc vat
eatPlants(Y):- eat(X,Y), classification(X,'Plants').

%lop dong vat ma trong do co it nhat 1 loai an thuc vat
classAnimalsEatPlants(Z):-eat(X,Y), classification(X,'Plants'),classification(Y,Z).

%Loai dong vat khong an thuc vat
eatAnimals(Y):- eat(X,Y), not(classification(X,'Plants')).

%Lop dong vat ma trong do co it nhat 1 loai khong an thuc vat
classAnimalsEatAnimals(Z):- eat(X,Y), not(classification(X,'Plants')),classification(Y,Z).

%Loai dong vat an tap
omnivorous(Y):- eat(X,Y), eat(T,Y), classification(X,'Plants'),not(classification(T,'Plants')).

%Lop dong vat ma trong do co loai an tap
classAnimalsCmnivorous(Z):- eat(X,Y), eat(T,Y), classification(X,'Plants'),not(classification(T,'Plants')),classification(Y,Z).

%Loai Y an lop C
eatClass(C,Y):- eat(X,Y), classification(X,C).

%Loai dong vat chi an thuc vat
eatOnlyPlants(Y):- eatPlants(Y), not(omnivorous(Y)).

%Lop dong vat ma co it nhat 1 loai chi an thuc vat
classEatOnlyPlants(Z):- eatPlants(Y), not(omnivorous(Y)), classification(Y,Z).

%Loai dong vat khong co ke thu
suzerain(Y):- eat(X,Y), not(eat(Y,Z)).
