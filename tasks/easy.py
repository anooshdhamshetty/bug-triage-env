from env.environment import BugTriageEnv


class EasyTask:
    def __init__(self):
        self.env = BugTriageEnv()
        self.name = "easy"

    def reset(self):
        return self.env.reset()

    def step(self, action):
        return self.env.step(action)

    def get_expected(self):
        return self.env.current_bug["expected"]