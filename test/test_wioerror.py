import pytest
import src.wio_errors as errors

def test_no_error():
    ans = b'+AT: OK\n'
    try:
        errors.wioError(ans)
        assert True
    except:
        assert False
@pytest.mark.parametrize(['ans','exception'],
                         [(b'+AT: ERROR(-10)\n',errors.Wioe5CommandUnkownError),
                          (b'+AT: ERROR(-11)\n',errors.Wioe5WrongFormatError),
                          (b'+AT: ERROR(-12)\n',errors.Wioe5CommandUnavailableError),
                          (b'+AT: ERROR(-20)\n',errors.Wioe5ExcessParametersError),
                          (b'+AT: ERROR(-21)\n',errors.Wioe5LenghtError),
                          (b'+AT: ERROR(-22)\n',errors.Wioe5TimeoutError),
                          (b'+AT: ERROR(-23)\n',errors.Wioe5InvalidCharError),
                          (b'+AT: ERROR(-24)\n',errors.Wioe5Error),
                          (b'+AT: ERROR(-1)\n',errors.Wioe5InvalidParameterError),
                          (b'+AT: ERROR(-10)\r\n',errors.Wioe5CommandUnkownError),
                          (b'+AT: ERROR(-11)\r\n',errors.Wioe5WrongFormatError),
                          (b'+AT: ERROR(-12)\r\n',errors.Wioe5CommandUnavailableError),
                          (b'+AT: ERROR(-20)\r\n',errors.Wioe5ExcessParametersError),
                          (b'+AT: ERROR(-21)\r\n',errors.Wioe5LenghtError),
                          (b'+AT: ERROR(-22)\r\n',errors.Wioe5TimeoutError),
                          (b'+AT: ERROR(-23)\r\n',errors.Wioe5InvalidCharError),
                          (b'+AT: ERROR(-24)\r\n',errors.Wioe5Error),
                          (b'+AT: ERROR(-1)\r\n',errors.Wioe5InvalidParameterError)])
def test_errors(ans,exception):
    try:
        errors.wioError(ans)
        assert False
    except exception:
        assert True
    except:
        assert False
