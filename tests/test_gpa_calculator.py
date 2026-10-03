import pytest

from sls_gpa_calculator_lib import calculate_gpa, GRADE_POINTS
from app.models import Enrollment, Course

@pytest.fixture
def three_credit_hour_course():
    single_course = Course(
        prefix="TEST",
        number="123",
        name="Test Course 1",
        credits=3
    )
    return single_course

@pytest.fixture
def four_credit_hour_course():
    single_course = Course(
        prefix="TEST",
        number="456",
        name="Test Course 2",
        credits=4
    )
    return single_course

@pytest.fixture
def malformed_course_no_credits():
    single_course = Course(
            prefix="TEST",
            number="456",
            name="Test Course 2",
        )
    return single_course

@pytest.fixture
def malformed_single_enrollment_missing_grade(three_credit_hour_course):
    single_enrollment = [Enrollment(
        user_id="teststudent",
        course_prefix="TEST",
        course_number="123",
        course=three_credit_hour_course
    )]
    return single_enrollment


@pytest.fixture
def malformed_single_enrollment_missing_credits(malformed_course_no_credits):
    single_enrollment = [Enrollment(
        user_id="teststudent",
        course_prefix="TEST",
        course_number="456",
        grade="A",
        course=malformed_course_no_credits
    )]
    return single_enrollment


@pytest.fixture
def malformed_single_enrollment_bad_grade(four_credit_hour_course):
    single_enrollment = [Enrollment(
        user_id="teststudent",
        course_prefix="TEST",
        course_number="456",
        grade="Z+",
        course=four_credit_hour_course
    )]
    return single_enrollment


@pytest.fixture
def single_enrollment(three_credit_hour_course):
    single_enrollment = [Enrollment(
        user_id="teststudent",
        course_prefix="TEST",
        course_number="123",
        grade="A+",
        course=three_credit_hour_course
    )]
    return single_enrollment


@pytest.fixture
def multiple_enrollments(three_credit_hour_course, four_credit_hour_course):
    multiple_enrollments = [
        Enrollment(
            user_id="teststudent",
            course_prefix="TEST",
            course_number="123",
            grade="A",
            course=three_credit_hour_course
        ),
        Enrollment(
            user_id="teststudent",
            course_prefix="TEST",
            course_number="456",
            grade="F",
            course=four_credit_hour_course
        ),
        Enrollment(
            user_id="teststudent",
            course_prefix="TEST",
            course_number="123",
            grade="B+",
            course=three_credit_hour_course
        ),
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
    credit_hours = sum(enrollment.course.credits for enrollment in multiple_enrollments)
    quality_grade_points = sum(
        GRADE_POINTS[enrollment.grade] * enrollment.course.credits for enrollment in multiple_enrollments
    )

    expected_gpa = quality_grade_points / credit_hours
    calculated_gpa = calculate_gpa(multiple_enrollments)
    assert expected_gpa == calculated_gpa


def test_gpa_calculation_ignores_missing_credits(
    malformed_single_enrollment_missing_credits,
):
    """
    Tests the calculation of the GPA will return 0.0 if
    malformed enrollments are returned.
    """
    assert 0.0 == calculate_gpa(malformed_single_enrollment_missing_credits)


def test_gpa_calculation_ignores_invalid_grade(malformed_single_enrollment_bad_grade):
    """
    Tests the calculation of the GPA will ignore an invalid
    grade and return a 0.0 GPA for that entry.
    """

    assert 0.0 == calculate_gpa(malformed_single_enrollment_bad_grade)


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
    malformed_single_enrollment_bad_grade,
):
    """
    Tests the calculation of multiple enrollments where one enrollment is properly
    formed and multiple enrollments are malformed.
    """
    enrollments = (
        single_enrollment
        + malformed_single_enrollment_missing_credits
        + malformed_single_enrollment_missing_grade
        + malformed_single_enrollment_bad_grade
    )

    assert 4.3 == calculate_gpa(enrollments)
