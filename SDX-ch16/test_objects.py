from io import StringIO
from textwrap import dedent
from objects import SaveObjects, LoadObjects  # Make sure to import these classes

# Tests for saving objects
def test_save_bool_single():
    output = StringIO()
    saver = SaveObjects(output)
    saver.save(True)
    assert output.getvalue() == "bool:True\n"

def test_save_dict_empty():
    output = StringIO()
    saver = SaveObjects(output)
    saver.save({})
    assert output.getvalue() == "dict:0\n"

def test_save_dict_flat():
    fixture = {"alpha": "beta", 1: 2}
    expected = dedent("""\
    dict:2
    str:1
    alpha
    str:1
    beta
    int:1
    int:2
    """)
    output = StringIO()
    saver = SaveObjects(output)
    saver.save(fixture)
    assert output.getvalue() == expected

def test_save_float_single():
    output = StringIO()
    saver = SaveObjects(output)
    saver.save(1.23)
    assert output.getvalue() == "float:1.23\n"

def test_save_int_single():
    output = StringIO()
    saver = SaveObjects(output)
    saver.save(-456)
    assert output.getvalue() == "int:-456\n"

def test_save_list_flat():
    fixture = [0, False]
    expected = dedent("""\
    list:2
    int:0
    bool:False
    """)
    output = StringIO()
    saver = SaveObjects(output)
    saver.save(fixture)
    assert output.getvalue() == expected

def test_save_str_single():
    fixture = dedent("""\
    a
    b
    c
    """)
    expected = dedent("""\
    str:4
    a
    b
    c

    """)
    output = StringIO()
    saver = SaveObjects(output)
    saver.save(fixture)
    assert output.getvalue() == expected

def test_save_set_flat():
    fixture = {1, "a"}
    first = dedent("""\
    set:2
    int:1
    str:1
    a
    """
    )
    second = dedent("""\
    set:2
    str:1
    a
    int:1
    """
    )
    output = StringIO()
    saver = SaveObjects(output)
    saver.save(fixture)
    actual = output.getvalue()
    assert actual in {first, second}

# Tests for loading objects
def test_load_bool_single():
    fixture = StringIO("bool:True\n")
    loader = LoadObjects(fixture)
    assert loader.load() == True

def test_load_dict_empty():
    fixture = StringIO("dict:0\n")
    loader = LoadObjects(fixture)
    assert loader.load() == {}

def test_load_dict_flat():
    fixture = StringIO(dedent("""\
        dict:2
        str:1
        alpha
        str:1
        beta
        int:1
        int:2
        """))
    loader = LoadObjects(fixture)
    assert loader.load() == {"alpha": "beta", 1: 2}

def test_load_float_single():
    fixture = StringIO("float:1.23\n")
    loader = LoadObjects(fixture)
    assert loader.load() == 1.23

def test_load_int_single():
    fixture = StringIO("int:-456\n")
    loader = LoadObjects(fixture)
    assert loader.load() == -456

def test_load_list_flat():
    fixture = StringIO(dedent("""\
    list:2
    int:0
    bool:False
    """))
    loader = LoadObjects(fixture)
    assert loader.load() == [0, False]

def test_load_str_single():
    fixture = StringIO(dedent("""\
    str:4
    a
    b
    c

    """))
    loader = LoadObjects(fixture)
    expected = dedent("""\
    a
    b
    c
    """)
    assert loader.load() == expected

def test_load_set_flat():
    fixture = StringIO(dedent("""\
    set:2
    int:1
    str:1
    a
    """))
    loader = LoadObjects(fixture)
    assert loader.load() == {1, "a"}

def test_roundtrip():
    fixture = ["a", {"b": 987.6}, {"c", True}]
    output = StringIO()
    saver = SaveObjects(output)
    saver.save(fixture)
    archive = output.getvalue()
    loader = LoadObjects(StringIO(archive))
    result = loader.load()
    assert result == fixture

