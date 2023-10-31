def test_grade(grade):
    if grade >= 90:
        print("Grade A")
    elif grade >= 80:
        print("Grade B")
    elif grade >= 70:
        print("Grade C")
    elif grade >= 60:
        print("Grade D")
    elif grade >= 50:
        print("Grade E")
    else:
        print("Grade F (failed)")

test_grade(89)
test_grade(99)
test_grade(45)