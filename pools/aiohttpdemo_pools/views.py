from aiohttp import web

import aiohttp_jinja2
import jinja2

#aiohttp_jinja2.setup(
#        app,
#        loader=jinja2.PackageLoader('aiohttp_pools', 'templates')
#    )

async def index(request):
    return web.Response(text="Hello Aiohttp!")

async def send_message():
    pass

@aiohttp_jinja2.template('detail.html')
async def pool(request):
    async with request['db'].acquire() as conn:
        question_id = request.match_info['question_id']
        try:
            question, choices = await db.get_question(
                    conn,
                    question_id
                )
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))
        return {
                'question': question,
                'choices': choices
            }
