from z3 import *


# formulas(assumptions).

# all x (Wolf(x) -> Animal(x)).
# all x (Fox(x) -> Animal(x)).
# all x (Bird(x) -> Animal(x)).
# all x (Caterpillar(x) -> Animal(x)).
# all x (Snail(x) -> Animal(x)).
# all x (Grain(x) -> Plant(x)).
S = Solver()
x = Bool('x')
y = Bool('y')
u = Bool('u')
z = Bool('z')


#Declarations have names, they are retrieved using the method name(). A (function) declaration has an arity, a domain and range sorts.
B = BoolSort()

Animal = Function('Animal', B, B)
Plant = Function('Plant', B, B)

Wolf = Function('Wolf', B, B)
Fox = Function('Fox', B, B)
Bird = Function('Bird', B, B)
Caterpillar = Function('Caterpillar', B, B)
Snail = Function('Snail', B, B)
Grain = Function('Grain', B, B)

#Everyone is either a Wolf or Fox or Bird or Cat. or Snail or Grain
S.add( ForAll(x, Or( Implies(x, Wolf(x)), Implies(x, Fox(x)), Implies(x, Bird(x)), Implies(x, Caterpillar(x)), Implies(x, Snail(x)), Implies(x, Grain(x))  ) ) )


# exists x Wolf(x).
# exists x Fox(x).
# exists x Bird(x).
# exists x Caterpillar(x).
# exists x Snail(x).
# exists x Grain(x).

S.add( Exists(x, Wolf(x)) )
S.add( Exists(x, Fox(x)) )
S.add( Exists(x, Bird(x)) )
S.add( Exists(x, Caterpillar(x)) )
S.add( Exists(x, Snail(x)) )
S.add( Exists(x, Grain(x)) )



# % All animals either eat all plants or eat all smaller animals
# % that eat some plants.

# all x (Animal(x) -> (all y (Plant(y) -> Eats(x,y)))
#                     | 
#                     (all z ( Animal(z) &
#                              Smaller(z,x) &
#                              (exists u (Plant(u) & Eats(z,u)))
#                             ->
#                              Eats(x,z)))).

Eats = Function('Eats', B, B, B)
Smaller = Function('Smaller', B, B, B)
S.add( ForAll(x, Implies(Animal(x), Or(
                                         ForAll(y, Implies(
                                                         Plant(y),
                                                         Eats(x,y))),
                                         ForAll(z, Implies(
                                                         And(
                                                            Animal(z),
                                                            Smaller(z,x),
                                                            Exists(u, And(
                                                                          Plant(u), Eats(z,u)
                                                                         )
                                                                  )
                                                            ),
                                                            Eats(x,z)))
                                      ) ) ) )

# all x all y (Caterpillar(x) & Bird(y) -> Smaller(x,y)).
# all x all y (Snail(x) & Bird(y) -> Smaller(x,y)).
# all x all y (Bird(x) & Fox(y) -> Smaller(x,y)).
# all x all y (Fox(x) & Wolf(y) -> Smaller(x,y)).
# all x all y (Bird(x) & Caterpillar(y) -> Eats(x,y)).

S.add( Implies( And( Caterpillar(x), Bird(y)), Smaller(x,y) ) )
S.add( Implies( And( Snail(x), Bird(y)), Smaller(x,y) ) )
S.add( Implies( And( Bird(x), Fox(y)), Smaller(x,y) ) )
S.add( Implies( And( Fox(x), Wolf(y)), Smaller(x,y) ) )
S.add( Implies( And( Bird(x), Caterpillar(y)), Eats(x,y) ) )




# all x (Caterpillar(x) -> (exists y (Plant(y) & Eats(x,y)))).
# all x (Snail(x)       -> (exists y (Plant(y) & Eats(x,y)))).
S.add( Implies( Caterpillar(x), Exists(y, And(Plant(y), Eats(x,y))) ) )
S.add( Implies( Snail(x), Exists(y, And(Plant(y), Eats(x,y))) ) )



# all x all y (Wolf(x) & Fox(y) -> -Eats(x,y)).
# all x all y (Wolf(x) & Grain(y) -> -Eats(x,y)).
# all x all y (Bird(x) & Snail(y) -> -Eats(x,y)).

S.add( Implies( And( Wolf(x), Fox(y)), Not( Eats(x,y)) ) )
S.add( Implies( And( Wolf(x), Grain(y)), Not( Eats(x,y)) ) )
S.add( Implies( And( Bird(x), Snail(y)), Not( Eats(x,y)) ) )


# end_of_list.

# formulas(goals).

# % There is an animal that eats {an animal that eats all grains}.

# exists x exists y ( Animal(x) &
# 	            Animal(y) &
# 	            Eats(x,y) &
#                     (all z (Grain(z) -> Eats(y,z)))).

S.add( Exists(x, Exists(
                        y,
                        And(
                            Animal(x),
                            Animal(y),
                            Eats(x,y),
                            ForAll( z, Implies(
                                               Grain(z),
                                               Eats(y,z)
                                              )
                                  )
                           )
                        )
             )
     )
# end_of_list.
#S.check()
print(S.check())
print(S.model())