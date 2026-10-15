from lab2_model import ClassroomAgent


def run_checks():
    agent = ClassroomAgent()
    cases = [
        ("first hot occupied room", (29, True), None, "COOL", True),
        ("same percept repeated", (29, True), "COOL", "COOL", False),
        ("lower boundary", (20, True), "COOL", "IDLE", True),
        ("upper boundary", (26, True), "IDLE", "IDLE", False),
        ("cold occupied room", (19, True), "IDLE", "WARM", True),
        ("empty room priority", (29, False), "WARM", "ECO", True),
        ("empty room repeated", (29, False), "ECO", "ECO", False),
    ]

    print("test | percept | expected previous | target | expected send | actual previous | actual target | actual send | result")
    for name, percept, expected_previous, expected_target, expected_send in cases:
        previous, target, send = agent.act(*percept)
        passed = (previous == expected_previous and
                  target == expected_target and send == expected_send)
        print(name, percept, expected_previous, expected_target,
              expected_send, previous, target, send,
              "PASS" if passed else "FAIL", sep=" | ")
        if not passed:
            raise AssertionError(f"Test failed: {name}")


if __name__ == "__main__":
    run_checks()
