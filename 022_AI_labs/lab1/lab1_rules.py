def check_application(score, documents_complete, identity_verified,
                      eligibility_confirmed):
    if not documents_complete:
        return "Hold"
    if score < 70:
        return "Hold"
    if not identity_verified:
        return "Hold"
    if not eligibility_confirmed:
        return "Hold"
    return "Review"


cases = [
    {
        "name": "pass_all_conditions",
        "score": 82,
        "documents_complete": True,
        "identity_verified": True,
        "eligibility_confirmed": True,
        "expected": "Review",
        "reason": "All four conditions pass."
    },
    {
        "name": "identity_not_verified",
        "score": 82,
        "documents_complete": True,
        "identity_verified": False,
        "eligibility_confirmed": True,
        "expected": "Hold",
        "reason": "Identity verification is missing."
    },
    {
        "name": "eligibility_not_confirmed",
        "score": 82,
        "documents_complete": True,
        "identity_verified": True,
        "eligibility_confirmed": False,
        "expected": "Hold",
        "reason": "Eligibility has not been confirmed."
    },
    {
        "name": "score_boundary",
        "score": 70,
        "documents_complete": True,
        "identity_verified": True,
        "eligibility_confirmed": True,
        "expected": "Review",
        "reason": "The score equals the inclusive threshold of 70."
    },
]

print("case | inputs | expected | actual | result | reason")
for case in cases:
    actual = check_application(
        case["score"],
        case["documents_complete"],
        case["identity_verified"],
        case["eligibility_confirmed"]
    )
    inputs = (
        f"score={case['score']}, documents_complete={case['documents_complete']}, "
        f"identity_verified={case['identity_verified']}, "
        f"eligibility_confirmed={case['eligibility_confirmed']}"
    )
    status = "PASS" if actual == case["expected"] else "FAIL"
    print(case["name"], inputs, case["expected"], actual, status,
          case["reason"], sep=" | ")
