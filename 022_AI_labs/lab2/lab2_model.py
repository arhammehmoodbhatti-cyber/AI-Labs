class ClassroomAgent:
    def __init__(self):
        self.previous_mode = None

    def act(self, temp, occupied):
        if not occupied:
            target_mode = "ECO"
        elif temp > 26:
            target_mode = "COOL"
        elif temp < 20:
            target_mode = "WARM"
        else:
            target_mode = "IDLE"

        send_command = target_mode != self.previous_mode
        previous_mode = self.previous_mode
        self.previous_mode = target_mode

        return previous_mode, target_mode, send_command


if __name__ == "__main__":
    agent = ClassroomAgent()
    percepts = [(29, True), (29, True), (20, True),
                (26, True), (19, True), (29, False)]

    print("step | previous mode | percept | target mode | command")
    for step, percept in enumerate(percepts, 1):
        previous, target, send = agent.act(*percept)
        command = "SEND" if send else "NO COMMAND"
        print(step, previous, percept, target, command, sep=" | ")
