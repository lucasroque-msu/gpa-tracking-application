*__disclaimer: This is a school project, not intended for true opensource development. Go Roadrunners, and go team Third Place!__*

# sls_gpa_calculator_lib
The `sls_gpa_calculator_lib` package makes it easy to calculate your GPA across multiple enrollments! You can easily calculate your academic GPA by leveraging `calculate_gpa` in your web application.

Example of running `calculate_gpa`:
```python
from sls_gpa_calculator_lib import calculate_gpa

enrollments = [
    Enrollment(...),
    Enrollment(...),
    ...
]

calculate_gpa(enrollments)
```

# Features
- Easily calculates a students GPA based on a list of of `Enrollments`.

# Bugs & New Features
Please use the [project's issue tracker](https://github.com/lucasroque-msu/gpa-tracking-application/issues) to submit bugs as well as new feature requests!


