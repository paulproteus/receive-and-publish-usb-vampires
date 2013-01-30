import bottle

@bottle.route('/submit/')
def submit():
    return "fail"

if __name__ == '__main__':
    bottle.run(host='localhost', port=8080)
