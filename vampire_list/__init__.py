import bottle

@bottle.route('/submit/')
def submit():
    return "fail"

@bottle.route('/')
def home():
    return 'Hello! Read <a href="https://github.com/paulproteus/receive-and-publish-usb-vampires/blob/master/README">README</a>.'

if __name__ == '__main__':
    bottle.run(host='localhost', port=8080)
