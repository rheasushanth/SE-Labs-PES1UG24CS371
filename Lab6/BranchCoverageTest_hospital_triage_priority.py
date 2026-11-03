import pytest
from hospital_triage_priority import process_triage_wards, monitor_oxygen_manifolds


def make_ward(patients, tier="general", icu_standby=False):
    return {
        "is_accepting": True,
        "tier": tier,
        "icu_standby": icu_standby,
        "patients": patients,
    }


def test_single_normal_patient():
    wards = [make_ward([{"spo2": 98, "hr": 72, "unconscious": False}])]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 10
    assert result["status"] == "TRIAGE_STABLE"


def test_wards_not_a_list_raises_error():
    with pytest.raises(ValueError):
        process_triage_wards("not a list", 10)


def test_ward_not_accepting_is_skipped():
    wards = [{"is_accepting": False, "patients": [{"spo2": 98, "hr": 72}]}]
    result = process_triage_wards(wards, 10)
    assert result == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_invalid_vitals_are_flagged_and_not_scored():
    wards = [make_ward([{"spo2": 0, "hr": 72}])]
    result = process_triage_wards(wards, 10)
    assert result == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_unconscious_patient_in_general_ward_scores_100():
    wards = [make_ward([{"spo2": 98, "hr": 72, "unconscious": True}])]
    result = process_triage_wards(wards, 10)
    assert result == {"acuity_score": 100, "status": "TRIAGE_STABLE"}


def test_unconscious_patient_in_outpatient_ward_resets_score():
    wards = [make_ward([{"spo2": 98, "hr": 72, "unconscious": True}], tier="outpatient")]
    result = process_triage_wards(wards, 10)
    assert result == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_low_spo2_scores_60():
    wards = [make_ward([{"spo2": 85, "hr": 72}])]
    result = process_triage_wards(wards, 10)
    assert result == {"acuity_score": 60, "status": "TRIAGE_STABLE"}


def test_icu_standby_adds_25():
    wards = [make_ward([{"spo2": 98, "hr": 72}], icu_standby=True)]
    result = process_triage_wards(wards, 10)
    assert result == {"acuity_score": 35, "status": "TRIAGE_STABLE"}


def test_more_than_four_flagged_entries_gives_ward_alert():
    wards = [make_ward([{"spo2": 0, "hr": 72}] * 5)]
    result = process_triage_wards(wards, 10)
    assert result == {"acuity_score": 0, "status": "WARD_ALERT"}


def test_monitor_no_data():
    assert monitor_oxygen_manifolds([]) == "NO_DATA"


def test_monitor_two_low_readings_in_a_row_is_failure():
    assert monitor_oxygen_manifolds([[3.5, 3.0]]) == "PRESSURE_FAILURE"


def test_monitor_all_normal_readings():
    assert monitor_oxygen_manifolds([[5.0, 4.5]]) == "PRESSURE_NORMAL"


# ---------- Extra tests for branch coverage and edge cases ----------

def test_negative_default_score_raises_error():
    with pytest.raises(ValueError):
        process_triage_wards([], -1)


def test_empty_wards_list_has_no_urgent_cases():
    assert process_triage_wards([], 10) == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_ward_without_is_accepting_key_is_skipped():
    wards = [{"patients": [{"spo2": 98, "hr": 72}]}]
    assert process_triage_wards(wards, 10)["acuity_score"] == 0


def test_accepting_ward_with_no_patients():
    wards = [make_ward([])]
    assert process_triage_wards(wards, 10) == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_invalid_heart_rate_is_flagged_and_not_scored():
    wards = [make_ward([{"spo2": 98, "hr": 0}])]
    assert process_triage_wards(wards, 10)["acuity_score"] == 0


def test_high_heart_rate_scores_60():
    wards = [make_ward([{"spo2": 98, "hr": 121}])]
    assert process_triage_wards(wards, 10)["acuity_score"] == 60


def test_boundary_vitals_use_default_score():
    # spo2 of exactly 90 and hr of exactly 120 are not treated as critical
    wards = [make_ward([{"spo2": 90, "hr": 120}])]
    assert process_triage_wards(wards, 10)["acuity_score"] == 10


def test_missing_patient_values_use_defaults():
    wards = [make_ward([{}])]
    assert process_triage_wards(wards, 10)["acuity_score"] == 10


def test_exactly_four_flagged_entries_is_not_an_alert():
    wards = [make_ward([{"spo2": 0, "hr": 72}] * 4)]
    assert process_triage_wards(wards, 10)["status"] == "NO_URGENT_CASES"


def test_outpatient_unconscious_stops_remaining_patients_in_that_ward():
    wards = [make_ward([{"spo2": 85, "hr": 72}, {"unconscious": True}, {"spo2": 85, "hr": 72}],
                       tier="outpatient")]
    assert process_triage_wards(wards, 10)["acuity_score"] == 0


def test_outpatient_reset_still_processes_next_ward():
    wards = [
        make_ward([{"unconscious": True}], tier="outpatient"),
        make_ward([{"spo2": 98, "hr": 72}]),
    ]
    assert process_triage_wards(wards, 10)["acuity_score"] == 10


def test_monitor_single_low_reading_is_normal():
    assert monitor_oxygen_manifolds([[3.5, 5.0]]) == "PRESSURE_NORMAL"


def test_monitor_streak_resets_after_normal_reading():
    assert monitor_oxygen_manifolds([[3.5, 5.0, 3.5]]) == "PRESSURE_NORMAL"


def test_monitor_exactly_4_bar_is_not_a_drop():
    assert monitor_oxygen_manifolds([[4.0, 4.0]]) == "PRESSURE_NORMAL"


def test_monitor_streak_does_not_carry_across_manifolds():
    assert monitor_oxygen_manifolds([[3.5], [3.5]]) == "PRESSURE_NORMAL"


def test_monitor_failure_in_later_manifold():
    assert monitor_oxygen_manifolds([[5.0], [3.5, 3.0]]) == "PRESSURE_FAILURE"


def test_monitor_empty_manifold_is_normal():
    assert monitor_oxygen_manifolds([[]]) == "PRESSURE_NORMAL"
