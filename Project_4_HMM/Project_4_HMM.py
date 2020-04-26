import copy
import decimal


class HMM:
    def __init__(self, observation: list, emission_prob: list, change_prob: int):
        self.observation = observation
        self.emission_prob = self.init_emission_prob(emission_prob)
        self.unchange_prob = change_prob

    def init_emission_prob(self, emission_prob) -> list:
        prob = []
        for list_val in emission_prob:
            temp = []
            for val in list_val:
                temp.append(decimal.Decimal(val))
            prob.append(temp)
        return prob

    def state_change_prob(self, pre_state: list, aim_dice: int) -> decimal.Decimal:
        prob = decimal.Decimal(0)
        for i in range(3):
            if i == aim_dice:
                prob += pre_state[i] * self.unchange_prob
            else:
                prob += pre_state[i] * (1 - self.unchange_prob) / 2
        return prob

    def forward(self, pre_state) -> list:
        prob = [decimal.Decimal(0) for _ in range(3)]
        for i in range(3):
        prob[i] = self.state_change_prob(pre_state, i)
        return prob

    def max_state(self, state_pro: list, obs_num) -> int:
        prob = copy.deepcopy(state_pro)

        for i in range(3):
            prob[i] *= self.emission_prob[i][obs_num - 1]
        max_value = prob[0]
        max_index = 0
        for i in range(1, 3):
            if max_value < prob[i]:
                max_value = prob[i]
                max_index = i
        return max_index

    def cal_state(self) -> list:
        state = []
        state_prob = [decimal.Decimal(1), decimal.Decimal(0), decimal.Decimal(0)]
        for i in range(0, len(self.observation)):
            state.append(self.max_state(state_prob, self.observation[i]) + 1)
            state_prob = self.forward(state_prob)
        index = self.max_state(state_prob, self.observation[99])
        print("pro:", state_prob[index])
        return state


def main():
    print("hello world!")
    observation = [1, 1, 2, 3, 3, 2, 3, 1, 2, 1, 3, 2, 1, 3, 2, 2, 1, 3, 3, 3, 2, 2, 3, 2, 3, 2, 3, 3, 1, 2, 3, 3, 3, 2,
                   2, 1, 3, 1, 2, 3, 1, 3, 1, 3, 1, 3, 1, 1, 2, 1, 1, 3, 2, 1, 3, 1, 2, 3, 2, 2, 3, 3, 3, 2, 1, 2, 3, 1,
                   2, 1, 2, 3, 1, 3, 2, 1, 1, 2, 2, 2, 2, 3, 2, 3, 3, 3, 1, 3, 1, 3, 3, 1, 2, 1, 1, 3, 2, 1, 3, 3
                   ]
    emission_prob = [
        [0.7, 0.15, 0.15],
        [0.15, 0.7, 0.15],
        [0.15, 0.15, 0.7]
    ]
    change_prob = 0
    correct_state = [1, 3, 1, 2, 1, 2, 3, 2, 3, 1, 2, 3, 1, 2, 1, 2, 1, 3, 2, 3, 1, 2, 3, 2, 1, 2, 1, 3, 1, 2, 3, 2, 1,
                     3, 2, 3, 2, 1, 2, 3, 1, 2, 1, 2, 1, 3, 1, 3, 2, 1, 2, 3, 2, 1, 2, 3, 2, 3, 1, 2, 3, 1, 3, 2, 1, 2,
                     3, 1, 2, 1, 2, 3, 1, 3, 1, 3, 2, 3, 2, 1, 2, 3, 2, 3, 1, 3, 2, 1, 2, 3, 1, 2, 1, 3, 2, 3, 2, 3, 1,
                     3]
    hmm = HMM(observation, emission_prob, change_prob)
    predict_state = hmm.cal_state()
    print("prediction:\n", predict_state)
    print("correct:\n", correct_state)
    num = 0
    for i in range(100):
        if predict_state[i] != correct_state[i]:
            num += 1
    print("wrong num: ", num)


if __name__ == "__main__":
    main()
