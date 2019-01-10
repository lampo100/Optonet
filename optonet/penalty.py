from optonet.consts import TRANSPONDER_CARDS


class DefaultPenaltyCalculator:

    MAX_TRANSPONDER_COST = max([card.cost for card in TRANSPONDER_CARDS])

    def calc_penalty(self, link_to_used_lambdas):
        penalty = 0
        for link, used_lambdas in link_to_used_lambdas.items():
            if link.capacity < used_lambdas:
                penalty += (used_lambdas - link.capacity) * DefaultPenaltyCalculator.MAX_TRANSPONDER_COST

        return penalty
