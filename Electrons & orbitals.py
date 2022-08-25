from itertools import permutations

number_of_electrons = 11
number_of_orbitals = 8
if not number_of_electrons > 2 * number_of_orbitals:
    if number_of_electrons < number_of_orbitals:
        number_of_free_orbitals = number_of_orbitals - number_of_electrons
        free_orbitals = list("0" * number_of_free_orbitals)
        electrons = list("1" * number_of_electrons)
        electrons.extend(free_orbitals)
        per = set(permutations(electrons))
        j = 0
        for i in per:
            print(i)
            j += 1
        print(j)
    elif number_of_electrons > number_of_orbitals:
        number_of_coupled_electrons = number_of_electrons - number_of_orbitals
        number_of_lone_electrons = number_of_orbitals - number_of_coupled_electrons
        lone_electrons = list("1" * number_of_lone_electrons)
        coupled_electrons = list("2" * number_of_coupled_electrons)
        coupled_electrons.extend(lone_electrons)
        per = set(permutations( coupled_electrons))
        j = 0
        for i in per:
            print(i)
            j += 1
        print(j)
    elif number_of_electrons == number_of_orbitals:
        boring_situation = list("1" * number_of_electrons)
        print(boring_situation)
else:
    print("Wrong configuration")
