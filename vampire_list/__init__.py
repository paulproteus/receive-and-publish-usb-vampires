import bottle
import os

@bottle.post('/')
def submit():
    print bottle.request.forms.get('payload')
    return "Saved as number ??"

@bottle.route('/read/')
def read_index():
    return "List them here"

@bottle.route('/read/:number')
def read(number=None):
    n = int(number)
    path = "data/%d.txt" % (n,)
    if not os.path.exists(path):
        return bottle.abort(404)
    return open(path).read()

@bottle.route('/')
def home():
    return 'Hello! Read <a href="https://github.com/paulproteus/receive-and-publish-usb-vampires/blob/master/README">README</a>.'

if __name__ == '__main__':
    bottle.run(host='localhost', port=8080)
