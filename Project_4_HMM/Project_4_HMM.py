import copy
import decimal


class HMM:
    def __init__(self, observation: list, emission_prob: list, unchange_prob: int):
        self.observation = observation
        self.emission_prob = self.init_emission_prob(emission_prob)
        self.unchange_prob = unchange_prob
        self.transition_prob = self.init_transition_prob(decimal.Decimal(unchange_prob))

    def init_emission_prob(self, emission_prob) -> list:
        prob = []
        for list_val in emission_prob:
            temp = []
            for val in list_val:
                temp.append(decimal.Decimal(val))
            prob.append(temp)

        return prob

    def init_transition_prob(self, unchange_prob):
        prob = []
        for i in range(3):
            temp = []
            for j in range(3):
                if i == j:
                    temp.append(unchange_prob)
                else:
                    temp.append((1 - unchange_prob) / 2)
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

    def forward(self, pre_state: list, obs_num: int) -> list:
        prob = [decimal.Decimal(0) for _ in range(3)]
        for i in range(3):
            prob[i] = self.state_change_prob(pre_state, i) * self.emission_prob[i][obs_num - 1]
        return prob

    def max_state(self, state_pro: list) -> int:

        max_value = state_pro[0]
        max_index = 0
        for i in range(0, 3):
            if max_value < state_pro[i]:
                max_value = state_pro[i]
                max_index = i
        return max_index

    def cal_state(self) -> list:
        state = []
        state_prob = [decimal.Decimal(1) * decimal.Decimal(0.7), decimal.Decimal(0) * decimal.Decimal(0.15),
                      decimal.Decimal(0) * decimal.Decimal(0.15)]
        state.append(self.max_state(state_prob) + 1)
        for i in range(0, len(self.observation) - 1):
            state_prob = self.forward(state_prob, self.observation[i + 1])
            state.append(self.max_state(state_prob) + 1)
        index = self.max_state(state_prob)
        print("pro:", state_prob[index])
        return state

    def viterbi(self) -> tuple:
        state_prob = [{}]
        path = {}

        for i in range(3):
            state_prob[0][i] = decimal.Decimal(1) / decimal.Decimal(3) * self.emission_prob[i][self.observation[0] - 1]
            path[i] = [i + 1]

        for state_num in range(1, 100):
            state_prob.append({})
            newpath = {}

            for i in range(3):

                (prob, state) = max([(state_prob[state_num - 1][j] * self.transition_prob[j][i] * self.emission_prob[i][self.observation[state_num] - 1], j) for j in range(3)])
                state_prob[state_num][i] = prob
                newpath[i] = path[state] + [i + 1]

            path = newpath

        (prob, state) = max([(state_prob[99][i], i) for i in range(3)])
        return prob, path[state]

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
    unchange_prob = 0
    correct_state = [1, 3, 1, 2, 1, 2, 3, 2, 3, 1, 2, 3, 1, 2, 1, 2, 1, 3, 2, 3, 1, 2, 3, 2, 1, 2, 1, 3, 1, 2, 3, 2, 1,
                     3, 2, 3, 2, 1, 2, 3, 1, 2, 1, 2, 1, 3, 1, 3, 2, 1, 2, 3, 2, 1, 2, 3, 2, 3, 1, 2, 3, 1, 3, 2, 1, 2,
                     3, 1, 2, 1, 2, 3, 1, 3, 1, 3, 2, 3, 2, 1, 2, 3, 2, 3, 1, 3, 2, 1, 2, 3, 1, 2, 1, 3, 2, 3, 2, 3, 1,
                     3]
    hmm = HMM(observation, emission_prob, unchange_prob)
    # predict_state = hmm.cal_state()
    print("observation:\n", observation)
    # print("prediction:\n", predict_state)
    print("correct:\n", correct_state)
    (prob, path) = hmm.viterbi()
    print("prediction:\n", path)
    print(prob)
    num = 0
    for i in range(100):
        if path[i] != correct_state[i]:
            num += 1
    print("wrong num: ", num)


if __name__ == "__main__":
    main()
