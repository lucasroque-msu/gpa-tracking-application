import pytest

from src.sls_gpa_calculator import calculate_gpa


@pytest.fixture
def malformed_single_enrollment_missing_grade():
    single_enrollment = [{"credits": 3}]
    return single_enrollment


@pytest.fixture
def malformed_single_enrollment_missing_credits():
    single_enrollment = [{"grade": "A"}]
    return single_enrollment


@pytest.fixture
def single_enrollment():
    single_enrollment = [{"credits": 3, "grade": "A+"}]
    return single_enrollment


@pytest.fixture
def multiple_enrollments():
    multiple_enrollments = [
        {
            "credits": 3,
            "grade": "A",
            "quality_points": 12.0,
        },
        {
            "credits": 4,
            "grade": "A",
            "quality_points": 16.0,
        },
        {
            "credits": 3,
            "grade": "B+",
            "quality_points": 9.9,
        },
    ]
    return multiple_enrollments


def test_gpa_calculation_success_single_enrollment(single_enrollment):
    """Tests the calculation of the GPA where only one enrollment exists."""
    gpa = calculate_gpa(single_enrollment)
    assert gpa == 4.3


def test_gpa_calculation_fail_results_in_zero():
    """Tests passing an empty enrollments list returns zero."""
    gpa = calculate_gpa([])
    assert gpa == 0.0


def test_gpa_calculation_success_on_multiple_enrollments(multiple_enrollments):
    """
    Tests the calculation of the GPA across multiple
    enrollments is successful.
    """
    credit_hours = sum(enrollment["credits"] for enrollment in multiple_enrollments)
    quality_grade_points = sum(
        enrollment["quality_points"] for enrollment in multiple_enrollments
    )

    expected_gpa = quality_grade_points / credit_hours
    calculated_gpa = calculate_gpa(multiple_enrollments)
    assert expected_gpa == calculated_gpa


def test_gpa_calculation_skips_empty_enrollment(single_enrollment):
    """
    Tests the calculation of the GPA will ignore an empty enrollment
    but still validate the passed legitimate enrollment.
    """
    single_enrollment.append({})

    calculated_gpa = calculate_gpa(single_enrollment)
    assert 4.3 == calculated_gpa


def test_gpa_calculation_ignores_missing_credits(
    malformed_single_enrollment_missing_credits,
):
    """
    Tests the calculation of the GPA will return 0.0 if
    malformed enrollments are returned.
    """
    assert 0.0 == calculate_gpa(malformed_single_enrollment_missing_credits)


def test_gpa_calculation_ignores_invalid_grade():
    """
    Tests the calculation of the GPA will ignore an invalid
    grade and return a 0.0 GPA for that entry.
    """
    malformed_enrollment = [{"grade": "Z+", "credits": 4}]

    assert 0.0 == calculate_gpa(malformed_enrollment)


def test_gpa_calculation_ignores_missing_grade(
    malformed_single_enrollment_missing_grade,
):
    """
    Tests the calculation of the GPA will ignore a missing
    grade and return a 0.0 GPA for that entry.
    """
    assert 0.0 == calculate_gpa(malformed_single_enrollment_missing_grade)


def test_gpa_calculation_only_calculates_complete_enrollment(
    single_enrollment, malformed_single_enrollment_missing_credits
):
    """
    Tests the calculation of multiple enrollments where one enrollment
    with missing credits is ignored.
    """
    enrollments = single_enrollment + malformed_single_enrollment_missing_credits

    assert 4.3 == calculate_gpa(enrollments)


def test_gpa_calculation_ignores_multiple_malformed_enrollments(
    single_enrollment,
    malformed_single_enrollment_missing_credits,
    malformed_single_enrollment_missing_grade,
):
    """
    Tests the calculation of multiple enrollments where one enrollment is properly
    formed and multiple enrollments are malformed.
    """
    enrollments = (
        single_enrollment
        + malformed_single_enrollment_missing_credits
        + malformed_single_enrollment_missing_grade
    )

    assert 4.3 == calculate_gpa(enrollments)
