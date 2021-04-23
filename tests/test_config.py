
def test_config_development(app):
    assert app.config["SQLALCHEMY_DATABASE_URI"] == 'sqlite:///:memory:'
    assert not app.config["S3_FOLDER"]
    assert not app.config["SERVER_NAME"]
    assert app.static_url_path == ""

