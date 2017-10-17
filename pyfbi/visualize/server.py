import os
import json
import tornado.web
from pyfbi.fbi_stat import FBIStat


class IndexHandler(tornado.web.RequestHandler):

    def initialize(self, stat_dir):
        self.stat_dir = stat_dir

    def get(self):
        stats = {}
        for f in os.listdir(self.stat_dir):
            if f.startswith("."):
                continue
            path = os.path.join(self.stat_dir, f)
            ss = FBIStat.read_stats(path)
            stats[f] = [s.to_dict() for s in ss]

        self.render("index.html", stats=json.dumps(stats))

    def post(self):
        pass


class Application(tornado.web.Application):

    def __init__(self, stat_dir):
        self.stat_dir = stat_dir
        handlers = [
            (r"/", IndexHandler, dict(stat_dir=self.stat_dir))
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret=os.environ.get("SECRET_TOKEN", "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__"),
            debug=True,
        )

        super(Application, self).__init__(handlers, **settings)
