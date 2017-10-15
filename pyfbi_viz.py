import os
import tornado
from pyfbi.visualize.server import Application
from tornado.options import define, options


define("port", default=3000, help="run on the given port", type=int)
define("stat_dir", default="stat_dir", help="watch the target dir", type=str)


def main():
    tornado.options.parse_command_line()
    stat_dir = ""
    if not options.stat_dir:
        raise Exception("You have to set the stat_dir")
    else:
        if os.path.isabs(options.stat_dir):
            stat_dir = options.stat_dir
        else:
            dir = os.getcwd()
            stat_dir = os.path.join(dir, options.stat_dir)

    if not os.path.isdir(stat_dir):
        raise Exception("{} does not exist.".format(stat_dir))

    app = Application(stat_dir)
    print("pyfbi is running on port {0}".format(options.port))        
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
