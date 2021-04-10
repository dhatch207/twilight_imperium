class calculator():
    
    def __init__(self):
        self.attacker = []
        self.defender = []
        self.attacker_hit_distribution = {}
        self.defender_hit_distribution = {}
        self.precomputed_rounds = {}
        

    def add_attacker(self):
        # stores attacker fleet information
        # fleet struct created by input, then passed into modifiers to get 2d list for computation
        self.attacker = [[5], [7], [7], [11]]
        
    def add_defender(self):
        self.defender = [[5], [5], [11], [11]]
    
    def calculate(self):
        # checks that we have fleets
        # applies modifiers
        # starts iterate_round
        # returns probabilities

        self.attacker_hit_distribution = self._hit_distribution(self.attacker)
        self.defender_hit_distribution = self._hit_distribution(self.defender)

        result = self._iterate_round(len(self.attacker_hit_distribution), len(self.defender_hit_distribution))

        return result
        

    def _hit_distribution(self, all_units_attacks):

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

    def _iterate_round(self, attacker_initial_units, defender_initial_units):
        # check if we hit a base case
        expected_result = [0, 0, 0]
        if attacker_initial_units > 0 and defender_initial_units <= 0:
            expected_result[0] = 1
            return expected_result
        elif attacker_initial_units <= 0 and defender_initial_units > 0:
            expected_result[2] = 1
            return expected_result
        elif attacker_initial_units <=0 and defender_initial_units <= 0:
            expected_result[1] = 1
            return expected_result

        misses = 0

        for attacker_hits, attacker_hits_probability in self.attacker_hit_distribution[attacker_initial_units].items():
            for defender_hits, defender_hits_probability in self.defender_hit_distribution[defender_initial_units].items():
                # need to account for abilities, cards etc to calculate the new number of remaining ships



                # need to adjust probabilities and skip recursion for case all ships miss
                if attacker_hits == 0 and defender_hits == 0:
                    misses += attacker_hits_probability * defender_hits_probability
                    continue

                # need new variable since *_initial_units is being used in loop 
                attacker_units_remaining = attacker_initial_units - defender_hits
                defender_units_remaining = defender_initial_units - attacker_hits

                # NEW method
                if (attacker_units_remaining, defender_units_remaining) in self.precomputed_rounds:
                    prior = self.precomputed_rounds[(attacker_units_remaining, defender_units_remaining)]
                else:
                    prior = self._iterate_round(attacker_units_remaining, defender_units_remaining)
                    self.precomputed_rounds[(attacker_units_remaining, defender_units_remaining)] = prior

                # OLD method (for comparison only, its a lot slower but useful for testing)
                #prior = iterate_round(attacker_units_remaining, defender_units_remaining)

                expected_result = [expected_result[i] + prior[i] * attacker_hits_probability * defender_hits_probability for i in range(3)]

        expected_result = [x / (1 - misses) for x in expected_result]

        return expected_result

c = calculator()
c.add_attacker()
c.add_defender()
result = c.calculate()
print(result)

