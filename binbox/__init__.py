from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    prefix = "binbo/"
    config = Configurator(settings=settings)
    config.add_static_view( prefix + 'static', 'static', cache_max_age=3600)
    
    config.add_route('home', '/' + prefix)
    config.add_route('post', '/' + prefix + 'post')
    config.add_route('list', '/' + prefix + 'list')

    #API

    config.add_route('api_list', '/' + prefix + 'json/list')
    config.add_route('api_file', '/' + prefix + 'json/file')
    config.scan()
    
    return config.make_wsgi_app()
