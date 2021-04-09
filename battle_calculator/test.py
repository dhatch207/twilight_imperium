import numpy as np


def hit_distribution(attacks):
    # initialize empty dictionary with correct shape
    result = {i+1:{j:0 for j in range(i+2)} for i in range(len(attacks))}
    
    for n, attack in enumerate(attacks, start=1):
        hit_p = (11 - attack) / 10
        miss_p = (attack - 1) / 10
        if n == 1:
            # if this is the first ship, initialize the dict
            result[1] = {0:miss_p, 1:hit_p}
            continue
        else:
            # otherwise, use the values for n-1 ships to calculate distributions after the nth ship
            for num_hits, probability in result[n - 1].items():
                result[n][num_hits] += probability * miss_p
                result[n][num_hits + 1] += probability * hit_p            
    return result    

def iterate_round(a_r, d_r):

    # recurse down number of remaining ships
    expected_result = np.zeros(3)
    if a_r > 0 and d_r <= 0:
        expected_result[0] = 1
        return expected_result
    elif a_r <= 0 and d_r > 0:
        expected_result[2] = 1
        return expected_result
    elif a_r <=0 and d_r <= 0:
        expected_result[1] = 1
        return expected_result

    misses = 0

    for a_hits, a_p in a_hit_distribution[a_r].items():
        for d_hits, d_p in d_hit_distribution[d_r].items():
            # need to account for abilities, cards etc to calculate the new number of remaining ships
            a_new = a_r - d_hits
            d_new = d_r - a_hits

            #### NEXT TASK
            # add a way to check the state vs known states (particularly starting)
            # Goal to solve 2 problems:
            # 1 - if we have a recurring state, we can reuse the calculated probabilities (DONE!)
            # i.e., calculation after 1-0 + 0-1 hits is the same as 1-1
            # 2 - we can know how many attacks to remove per hit assigned (needed for implementation of ships with multiple attacks / sustain)
            # figure out how to remove more than one when a hit is assigned

            ### once this is figured out, we can graduate to calculator.py and move everything to a class


            # need to adjust probabilities and skip recursion for case all ships miss
            if a_hits == 0 and d_hits == 0:
                misses += a_p * d_p
                continue

            a_n_r = a_r - d_hits
            d_n_r = d_r - a_hits

            # NEW method
            if (a_n_r, d_n_r) in precomputed_rounds:
                prior = precomputed_rounds[(a_n_r, d_n_r)]
            else:
                prior = iterate_round(a_n_r, d_n_r)
                precomputed_rounds[(a_n_r, d_n_r)] = prior
            
            # OLD method (for comparison only, its a lot slower but useful for testing)
            #prior = iterate_round(a_n_r, d_n_r)

            expected_result += prior * a_p * d_p

    expected_result = expected_result / (1 - misses)

    return expected_result

#### RUNTIME ONLY BELOW ###

#(this should probably all get put into a class)

# ships = { id: {'type' = 'cruiser', 'attacks' = [7]} ] }
# need something to convert human inputs into this structure
attacker = {1: {'type':'cruiser', 'attacks':[7]}, 2: {'type':'cruiser', 'attacks':[7]}, 3: {'type':'cruiser', 'attacks':[7]}, 4: {'type':'cruiser', 'attacks':[7]},\
    5: {'type':'cruiser', 'attacks':[7]}, 6: {'type':'cruiser', 'attacks':[7]}, 7: {'type':'cruiser', 'attacks':[7]}}#,\
        #8: {'type':'cruiser', 'attacks':[7]}, 9: {'type':'cruiser', 'attacks':[7]}, 10: {'type':'cruiser', 'attacks':[7]},\
        #    11: {'type':'cruiser', 'attacks':[7]}, 12: {'type':'cruiser', 'attacks':[7]}, 13: {'type':'cruiser', 'attacks':[7]}}
defender = {1: {'type':'cruiser', 'attacks':[7]}, 2: {'type':'cruiser', 'attacks':[7]}, 3: {'type':'cruiser', 'attacks':[7]}, 4: {'type':'cruiser', 'attacks':[7]},\
    5: {'type':'cruiser', 'attacks':[7]}, 6: {'type':'cruiser', 'attacks':[7]}, 7: {'type':'cruiser', 'attacks':[7]},\
        8: {'type':'cruiser', 'attacks':[7]}, 9: {'type':'cruiser', 'attacks':[7]}, 10: {'type':'cruiser', 'attacks':[7]},\
            11: {'type':'cruiser', 'attacks':[7]}, 12: {'type':'cruiser', 'attacks':[7]}, 13: {'type':'cruiser', 'attacks':[7]}}

# convert to format for hit_distribution
a = [v for x in attacker.values() for v in x['attacks']]
d = [v for x in defender.values() for v in x['attacks']]

# keep track of how many attacks we lose per hit
# good because we can make this >1 for ships with more than one hit, and 0 for dummy sustain damage ships
a_num_attacks_lost_after_nth_hit = [len(x['attacks']) for x in attacker.values()]
d_num_attacks_lost_after_nth_hit = [len(x['attacks']) for x in defender.values()]

print(a_num_attacks_lost_after_nth_hit)
print(d_num_attacks_lost_after_nth_hit)

a_hit_distribution = hit_distribution(a)
d_hit_distribution = hit_distribution(d)

# stores computational results for iterate_round, remember to make it a class variable
precomputed_rounds = {}

print(iterate_round(len(a), len(d)))