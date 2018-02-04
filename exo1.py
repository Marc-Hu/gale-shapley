#!/usr/bin/env python
# -*- coding: utf-8 -*-

PREFS_IDX = 0
IS_FREE_IDX = 1
NO_APPLIED_IDX = 2


def read_file(s):  # Definition d'une fonction, avec un parametre (s). Ne pas oublier les ":"
    my_file = open(s, "r")  # Ouverture en lecture. Indentation par rapport a la ligne d'avant (<-> bloc).
    content = my_file.readlines()  # Contenu contient une liste de chainces de caracteres, chaque chaine correspond a une ligne
    my_file.close()  # Fermstdre du fichier
    leng = len(content)
    for i in range(leng):
        content[i] = content[i].split()
    return content


def open_pref(my_file, nb_ligne_a_suppr):
    content = read_file(my_file)
    capacity = None
    if my_file == "prefSpe.txt":
        capacity = content[1][1:]
        capacity = list(map(int, capacity))
    content = content[nb_ligne_a_suppr:]  # Supprimer les premières ligne des fichier (NbEtu 11)
    leng = len(content)
    for i in range(leng):
        prefs = list(map(int, content[i][2:]))
        content[i] = [prefs, True, 0]

    return content, capacity


def choose_first_match(pref):
    for i in range(len(pref)):
        if is_free(pref, i):
            return pref[i]
    return None


def is_free(pref, index):
    return pref[index][IS_FREE_IDX]


def propose(proposer, capacity=None):
    # get the number of chosen masters
    # get the first master chosen by the student in which he didn't apply yet
    print("proposer = ",proposer)
    index = proposer[PREFS_IDX][proposer[NO_APPLIED_IDX]]
    proposer[NO_APPLIED_IDX] = proposer[NO_APPLIED_IDX] + 1
    limit = -1
    if capacity is None:
        limit = len(proposer[PREFS_IDX])

    else:
        limit = capacity

    if proposer[NO_APPLIED_IDX] == limit:
        print("limit reached",proposer)
        proposer[IS_FREE_IDX] = False
    return index


def match(first_match, second_match, capacity=None):
    first_match[IS_FREE_IDX] = False
    second_match[NO_APPLIED_IDX] = second_match[NO_APPLIED_IDX] + 1

    if capacity is not None:
        if second_match[NO_APPLIED_IDX] == capacity:
            second_match[IS_FREE_IDX] = False
    else:
        second_match[IS_FREE_IDX] = False


def unmatch(first_match, second_match):
    first_match[IS_FREE_IDX] = True
    second_match[NO_APPLIED_IDX] = second_match[NO_APPLIED_IDX] - 1
    if second_match[NO_APPLIED_IDX] < 0:
        raise ValueError("NO_APPLIED_IDX can't be negative!")

    second_match[IS_FREE_IDX] = True


def old_matches(second_match, result):
    old_matches_indexes = []
    for couple in result:
        if couple[1] == second_match:
            old_matches_indexes.append(couple[0])

    return old_matches_indexes


def prefer(second_match, current_proposer_idx, pref, old_first_matches_indexes):
    for old_first_match_index in old_first_matches_indexes:
        if second_match[PREFS_IDX].index(current_proposer_idx) < second_match[PREFS_IDX].index(old_first_match_index):
            unmatch(pref[old_first_match_index], second_match)
            return True

    return False


def replace(second_match_index, result):
    for i in range(len(result)):
        if second_match_index == result[i][1]:
            return i
    return -1


# [[0, 5], [1, 6], [10, 4], [7, 7], [4, 1], [5, 0], [3, 0], [9, 2], [2, 8], [6, 8], [8, 3]]
# [[0, 5], [1, 6], [10, 4], [7, 7], [4, 1], [5, 0], [3, 0], [9, 2], [2, 8], [6, 8], [8, 3]]

def gale_shapley_impl(first_match_prefs, second_match_prefs, capacity, reversed):
    result = []  # this will hold tuple of our result (Student,Master)

    current_first_match = choose_first_match(first_match_prefs)  # choose a student
    while current_first_match is not None:  # while there is a student

        first_match_index = first_match_prefs.index(current_first_match)
        if reversed:
            second_match_index = propose(current_first_match, capacity[first_match_index])
        else:
            second_match_index = propose(current_first_match)

        if is_free(second_match_prefs, second_match_index):  # if the master is not full yet
            # enroll the student in this master # add it to the result
            # increment student applied masters
            # make student taken
            result.append([first_match_index, second_match_index])
            if reversed:
                match(current_first_match, second_match_prefs[second_match_index], capacity[first_match_index])
            else:
                match(current_first_match, second_match_prefs[second_match_index], capacity[second_match_index])
        elif prefer(second_match_prefs[second_match_index], first_match_index, first_match_prefs,
                    old_matches(second_match_index, result)):
            result[replace(second_match_index, result)][0] = first_match_index

            if reversed:
                match(current_first_match, second_match_prefs[second_match_index], capacity[first_match_index])
            else:
                match(current_first_match, second_match_prefs[second_match_index], capacity[second_match_index])
        else:
            continue
        current_first_match = choose_first_match(first_match_prefs)

    return result


def student_gale_shapley(student_prefs, master_prefs):
    return gale_shapley_impl(student_prefs[0], master_prefs[0], master_prefs[1],False)


def masters_gale_shapley(student_prefs, master_prefs):
    return gale_shapley_impl(master_prefs[0], student_prefs[0], master_prefs[1], True)


def print_grid(grid):
    for row in grid:
        if row is not None:
            for e in row:
                print(e, )
        print()


if __name__ == '__main__':
    pref_master = open_pref("prefSpe.txt", 2)
    pref_std = open_pref("prefEtu.txt", 1)
    print_grid(pref_master)
    print_grid(pref_std)
    result = student_gale_shapley(pref_std, pref_master)
    print(result)
    # result = masters_gale_shapley(pref_std, pref_master)
    # print(result)
