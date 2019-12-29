import hello

def test_hello():
    assert hello.hello_world("World!") == "Hello World!"

def test_user_is_greeted_on_launch(capsys):
    hello.launch()
    captured = capsys.readouterr()
    assert "Welcome" in captured.out
