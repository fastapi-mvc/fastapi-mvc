from fastapi_mvc.exceptions import RootException, FileError


def test_root_exception():
    ex = RootException("Where was Gondor when the Westfold fell?!")

    assert ex.code == 1
    assert ex.message == "Where was Gondor when the Westfold fell?!"
    assert str(ex) == "Where was Gondor when the Westfold fell?!"
    assert isinstance(ex, Exception)


def test_file_error():
    ex = FileError("This is not the file you are looking for")
    assert isinstance(ex, RootException)
