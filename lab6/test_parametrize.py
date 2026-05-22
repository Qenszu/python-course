
def validate_name(name):
    if not isinstance(name, str):
        raise ValueError("Imie musi byc typu string")
    if name == "":
        raise ValueError("Imie nie moze byc puste")
    return True

def validate_age(age):
    if not isinstance(age, int):
        raise ValueError("Wiek musi byc liczba calkowita")
    if age < 18:
        raise ValueError("Wiek nie moze byc mniejszy od 18")
    return True

def validate_email(email):
    if not isinstance(email, str):
        raise ValueError("Email musi byc typu string")
    if "@" not in email:
        raise ValueError("Email musi zawierac @")
    if "." not in email.split("@")[-1]:
        raise ValueError("Email po znaku @ musi zawierac znak .")
    return True

def validate_user(name, age, email):
    validate_name(name) 
    validate_age(age) 
    validate_email(email)

    return True 




import pytest

@pytest.mark.parametrize(
        "name, raise_exception",
        [
            ("Czarek", False),
            ("", True),
            (18, True),
            ("Kamil", False)
        ]
)
def test_name(name, raise_exception):
    if raise_exception:
        with pytest.raises(ValueError):
            validate_name(name)
    else:
        assert validate_name(name) is True

@pytest.mark.parametrize(
        "age, raise_exception",
        [
            ("Czarek", True),
            (17, True),
            (18, False),
            (58, False),
            (56.3, True)
        ]
)
def test_name(age, raise_exception):
    if raise_exception:
        with pytest.raises(ValueError):
            validate_age(age)
    else:
        assert validate_age(age) is True

@pytest.mark.parametrize(
        "email, raise_exception",
        [
            ("Czarek", True),
            (17, True),
            ("Czarek@AGH.pl", False),
            ("Czarek.AGH.pl", True),
            ("Czarek@AGHpl", True)
        ]
)
def test_name(email, raise_exception):
    if raise_exception:
        with pytest.raises(ValueError):
            validate_email(email)
    else:
        assert validate_email(email) is True
