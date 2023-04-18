import pytest
import src.wio_errors as errors

def test_no_error():
    ans = '+AT: OK\n'
    try:
        errors.wioError(ans)
        assert True
    except:
        assert False
@pytest.mark.parametrize(['ans','exception'],
                         [('+AT: ERROR(-10)\n',errors.Wioe5CommandUnkownError),
                          ('+AT: ERROR(-11)\n',errors.Wioe5WrongFormatError),
                          ('+AT: ERROR(-12)\n',errors.Wioe5CommandUnavailableError),
                          ('+AT: ERROR(-20)\n',errors.Wioe5ExcessParametersError),
                          ('+AT: ERROR(-21)\n',errors.Wioe5LenghtError),
                          ('+AT: ERROR(-22)\n',errors.Wioe5TimeoutError),
                          ('+AT: ERROR(-23)\n',errors.Wioe5InvalidCharError),
                          ('+AT: ERROR(-24)\n',errors.Wioe5Error),
                          ('+AT: ERROR(-1)\n',errors.Wioe5InvalidParameterError),
                          ('+AT: ERROR(-10)\r\n',errors.Wioe5CommandUnkownError),
                          ('+AT: ERROR(-11)\r\n',errors.Wioe5WrongFormatError),
                          ('+AT: ERROR(-12)\r\n',errors.Wioe5CommandUnavailableError),
                          ('+AT: ERROR(-20)\r\n',errors.Wioe5ExcessParametersError),
                          ('+AT: ERROR(-21)\r\n',errors.Wioe5LenghtError),
                          ('+AT: ERROR(-22)\r\n',errors.Wioe5TimeoutError),
                          ('+AT: ERROR(-23)\r\n',errors.Wioe5InvalidCharError),
                          ('+AT: ERROR(-24)\r\n',errors.Wioe5Error),
                          ('+AT: ERROR(-1)\r\n',errors.Wioe5InvalidParameterError)])
def test_errors(ans,exception):
    try:
        errors.wioError(ans)
        assert False
    except exception:
        assert True
    except:
        assert False
