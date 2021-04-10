import numpy as np


def hit_distribution(all_units_attacks):

    # flatten attacks to make the loop cleaner
    attacks = [x for y in all_units_attacks for x in y]
    # initialize empty struct for storage
    attack_distribution = {i+1:{j:0 for j in range(i+2)} for i in range(len(attacks))}

    for n, attack in enumerate(attacks, start=1):
        hit_p = (11 - attack) / 10
        miss_p = (attack - 1) / 10
        if n == 1:
            # if this is the first attack, initialize the dict
            attack_distribution[1] = {0:miss_p, 1:hit_p}
            continue
        else:
            # otherwise, use the values for n-1 attacks to calculate distributions after the nth attack
            for num_hits, probability in attack_distribution[n - 1].items():
                attack_distribution[n][num_hits] += probability * miss_p
                attack_distribution[n][num_hits + 1] += probability * hit_p

    # store result in terms of number of units, rather than number of attacks
    result = {}
    total_attacks_made = 0
 
    for unit, unit_attacks in enumerate(all_units_attacks, start=1):
        for attack in unit_attacks:
            total_attacks_made += 1
        result[unit] = attack_distribution[total_attacks_made]

    return result

def iterate_round(a_r, d_r):
### recurses over the number of ships remaining in battle ###

    # check if we hit a base case
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


a_2d =  [[5], [5], [11], [11]]
d_2d = [[7], [7], [7], [7]]

a_hit_distribution = hit_distribution(a_2d)
d_hit_distribution = hit_distribution(d_2d)

print(a_hit_distribution, '\n')
print(d_hit_distribution, '\n')

# stores computational results for iterate_round, remember to make it a class variable
precomputed_rounds = {}

print(iterate_round(len(a_hit_distribution), len(d_hit_distribution)))