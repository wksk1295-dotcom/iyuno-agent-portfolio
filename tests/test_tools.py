from agent.tools import calculator, policy_lookup
def test_calculator():
    assert calculator("2 + 3 * 4")["result"] == 14
def test_policy_lookup():
    assert "minimum" in policy_lookup("least_privilege")["result"]
