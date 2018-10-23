def get_config():
    from .development import DevelopmentConfig
    _config = DevelopmentConfig()

    return _config
