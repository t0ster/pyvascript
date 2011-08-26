import os
import sys
import time

try:
    from watchdog.observers import Observer
    from watchdog.events import PatternMatchingEventHandler
except ImportError:
    print >>sys.stderr, "Please install watchdog to use this feature."
    sys.exit(1)    

from pyvascript.utils.compile import compile_pyva


class PyvaHandler(PatternMatchingEventHandler):
    def __init__(self, patterns=[r"*.pyva"], *args, **kwargs):
        super(PyvaHandler, self).__init__(patterns, *args, **kwargs)
        
    def on_modified(self, event):
        file_path, _ = os.path.splitext(event.src_path)
        js_file_path = "%s.js" % file_path
        pyva_source = open(event.src_path).read()
        try:
            js_source = compile_pyva(pyva_source)
        except Exception, exc:
            print >>sys.stderr, "%s: %s" % (event.src_path, exc)
            return
        with open(js_file_path, "w+") as f:
            f.write(js_source)

        print("Compiled %s" % event.src_path)


def watch(path):    
    event_handler = PyvaHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main():
    if  len(sys.argv) > 2 or (len(sys.argv) == 2 and sys.argv[1] == "-h"):
        print >>sys.stderr, 'Usage: %s [path]' % sys.argv[0]
        sys.exit(1)

    if len(sys.argv) == 1:
        path = "."
    watch(path)


if __name__ == '__main__':
    main()
