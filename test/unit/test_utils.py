from labkey.utils import btoa, encode_uri_component, waf_encode


def test_btoa():
    assert btoa(None) is None
    assert btoa("") == ""
    assert btoa("DELETE TABLE some.table;") == "REVMRVRFIFRBQkxFIHNvbWUudGFibGU7"


def test_encode_uri_component():
    assert(
        encode_uri_component("SELECT * FROM x.y WHERE y = 5 & 2 AND y IS NOT NULL;")
        == "SELECT%20*%20FROM%20x.y%20WHERE%20y%20%3D%205%20%26%202%20AND%20y%20IS%20NOT%20NULL%3B"
    )
    assert encode_uri_component("><&/%' \"1äöüÅ") == "%3E%3C%26%2F%25'%20%221%C3%A4%C3%B6%C3%BC%C3%85"


def test_waf_encode():
    prefix = "/*{{base64/x-www-form-urlencoded/wafText}}*/"
    assert waf_encode(None) is None
    assert waf_encode("") == ""
    assert waf_encode("hello") == prefix + "aGVsbG8="
    assert waf_encode("DELETE TABLE some.table;") == prefix + "REVMRVRFJTIwVEFCTEUlMjBzb21lLnRhYmxlJTNC"
    assert waf_encode("><&/%' \"1äöüÅ") == prefix + "JTNFJTNDJTI2JTJGJTI1JyUyMCUyMjElQzMlQTQlQzMlQjYlQzMlQkMlQzMlODU="
