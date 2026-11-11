from hypothesis import given, strategies as st
from processor import parse_vitals_summary, compute_patient_bmi, assign_ward_bed

bmi_inputs = st.builds(lambda w, h: f"{w}/{h}", st.floats(), st.floats())
ward_inputs = st.builds(lambda w, n: f"{w}-{n}", st.text(), st.text())

@given(st.text() | st.none())
def test_parse_vitals_summary_no_crash(s):
    try:
        parse_vitals_summary(s)
    except (ValueError, TypeError):
        pass
    except Exception as e:
        assert False, f"parse_vitals_summary crashed with {type(e).__name__}: {e}"

@given(bmi_inputs)
def test_compute_patient_bmi_safe(s):
    try:
        compute_patient_bmi(s)
    except (ValueError, TypeError):
        pass
    except Exception as e:
        assert False, f"compute_patient_bmi crashed with {type(e).__name__}: {e}"

@given(ward_inputs)
def test_assign_ward_bed_safe(s):
    try:
        assign_ward_bed(s)
    except (ValueError, TypeError):
        pass
    except Exception as e:
        assert False, f"assign_ward_bed crashed with {type(e).__name__}: {e}"