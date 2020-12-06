#from views import index
from functools import partial

import views

def setup_routes(app, loop):
    index = partial(views.generate_index, loop=loop)
    app.router.add_get('/', index)
