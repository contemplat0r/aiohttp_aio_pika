from functools import partial

import views

#def setup_routes(app):
def setup_routes(app, pika_connection_proxy):
    print("setup_routes")
    #index = partial(views.generate_index, exchange=app['exchange'])
    index = partial(views.generate_index, exchange=pika_connection_proxy.exchange)
    app.router.add_get('/', index)
