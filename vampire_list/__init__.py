import bottle
import os
import glob
import tempfile
import tarfile

MAGIC_STRING = "Save us from vampires"

def get_data_path():
    return os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..', 'data'))

def find_next_available_data_path(i_start=0):
    i = i_start
    while True:
        try:
            os.mkdir(get_data_path()+ "/%d" % (i,))
            # Yay, it worked! Return.
            return i
        except OSError, e:
            if e.errno == 17:
                # Already exists. OK, increment, and loop.
                i += 1
            else:
                raise # What the heck is going on?

@bottle.post('/')
def submit():
    s = bottle.request.forms.get('payload')
    # Check for our magic string
    if MAGIC_STRING not in s:
        return bottle.abort(403, "Missing magic string")

    num = find_next_available_data_path()
    with open(get_data_path() + "/%d/txt" % (num,), 'w') as fd:
        fd.write(s)
    return bottle.redirect("/read/%d" % (
            num,))

@bottle.route('/read/')
def read_index():
    things = sorted([int(x.rsplit('/', 2)[1])
                     for x in glob.glob(get_data_path() + "/*/txt")])
    s = "<ul>"
    for thing in things:
        s += '<li><a href="/read/%d">%d</a></li>' % (
            thing, thing)
    s += "</ul>"
    s += '<p>Or, <a href="/tarball/">get a tarball</a>.</p>'
    return s

@bottle.route('/tarball/')
def tarball():
    ## Create tar file
    filename = tempfile.NamedTemporaryFile(delete=False).name
    tar = tarfile.open(filename, "w:gz")
    for txtpath in sorted(glob.glob(get_data_path() + "/*/txt")):
        number = txtpath.rsplit('/', 2)[1]
        tar.add(txtpath, arcname=number + ".txt")
    tar.close()

    ## Horrible (-: Return it to the user
    with open(filename) as fd:
        bottle.response.set_header('Content-Type', 'application/x-tar')
        return fd.read()

@bottle.route('/read/:number')
def read(number=None):
    n = int(number)
    path = get_data_path() + "/%d/txt" % (n,)
    if not os.path.exists(path):
        return bottle.abort(404)
    bottle.response.set_header('Content-Type', 'text/plain')
    return open(path).read()

@bottle.route('/')
def home():
    return 'Hello!<p>Read <a href="https://github.com/paulproteus/receive-and-publish-usb-vampires/blob/master/README">README</a>.</p><p>Or look at the <a href="/read/">list of posts</a>.</p>'

if __name__ == '__main__':
    bottle.run(host='localhost', port=8080)

application = bottle.default_app()
