import urllib2
import urllib

url = 'http://localhost:8080/'
data = urllib.urlencode({
        'payload': '''Something with
newlines
X-Agenda: Save us from vampires'''})

req = urllib2.Request(url, data, {})
print urllib2.urlopen(req).read()
