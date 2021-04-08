from queue import PriorityQueue

def compute_outcomes(attacker, defender):
    return None
    # attacker, defender =  [['shipType', [list of combat values], modifiedby, capacity]]

    # instead of splitting the tree ship by ship, go by total number of hits produced
    # to do this, we need to make a distribution of # of hits
    # for the future, we might be able to estimate the tails of this distribution

    # possibility: for each number of hits, compute the likelihood that this fleet gets that many hits
        # then we get an easy cut on the tails, once the likelihood of a # of hits is small enough we estimate the rest

    # then, given that number of hits we make the new list with the ships that are list and that probability
    

    # returns superset = {(attacker, defender): probability}

def permanent_modifiers(attacker, defender):
    # some modifiers are for this round, others are persistent
    # therefore we will also store the amount by which it needs to move to reset.

    # in the first round only:
        # apply faction / tech / and whatnot
        # space cannon, AFB, other abilities

    # every other round we check for a temporary modifiers


    return attacker, defender

def temporary_modifiers(attacker, defender):

    return attacker, defender

def iterate_round(attacker, defender):
    expected_result = [0, 0, 0]

    # check if one or both fleets are empty, in which case we have a result
    if attacker and not defender:
        expected_result = [1,0,0]
    elif defender and not attacker:
        expected_result = [0,0,1]
    elif not attacker and not defender:
        expected_result = [0,0,0] 
    else:
        # otherwise, we need to compute the possible outcomes of this round

        modified_attacker, modified_defender = temporary_modifiers(attacker, defender)
        outcomes = compute_outcomes(modified_attacker, modified_defender)

        # then we use the probability of each possible outcome and the result of that outcome to descend the probability tree
        for (attacker, defender), probability in outcomes.items():
            expected_result += (iterate_round(attacker, defender)) * probability

    return expected_result
    

def main():
    test_attacker = PriorityQueue()
    test_defender = PriorityQueue()

    test_attacker.put((7, ['cruiser', [7], 0]))

    test_attacker, test_defender = permanent_modifiers(test_attacker, test_defender)
    result = iterate_round(test_attacker, test_defender)

    print(result)


main()

# sustain damage adds a zero-cost ship with no combat value, if risk direct hit is off it has cost deadnought-1
# cost of carriers needs to change depending on capacity (i.e., the cost of a carrier needs to include what it's carrying)

# input is dict {'unit':quantity}
# keep list of default values for ships, such as ['cruiser', [7], 0, 0] then add them to the fleet as they come in by quantity