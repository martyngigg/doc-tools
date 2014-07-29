import getpass
import httplib
import mwclient
import urlparse
 
def get_server_status_code(url):
    """
    Download just the header of a URL and
    return the server's status code.
    """
    # http://stackoverflow.com/questions/1140661
    host, path = urlparse.urlparse(url)[1:3]    # elems [1] and [2]
    try:
        conn = httplib.HTTPConnection("wwwcache.rl.ac.uk",8080)
        conn.request('HEAD', url)
        return conn.getresponse().status
    except StandardError:
        return None
 
def check_url(url):
    """
    Check if a URL exists without downloading the whole file.
    We only check the URL header.
    """
    # see also http://stackoverflow.com/questions/2924422
    good_codes = [httplib.OK, httplib.FOUND, httplib.MOVED_PERMANENTLY]
    status = get_server_status_code(url)
    if status in good_codes:
        return True
    elif status == httplib.NOT_IMPLEMENTED and "github" in url:
        return True
    else:
        return False

def check_extlinks_on_all(site, contents_page):
    contents = site.Pages[contents_page]
    for item in contents.links():
        item_page = site.Pages[item.page_title]
        check_extlinks(site, item_page)

def check_extlinks(site, page):
    print "Checking",page.page_title
    extlinks = page.extlinks()
    working, broken = [], []
    for link in extlinks:
        if check_url(link):
            working.append(link)
        else:
            broken.append(link)
    ###
    if len(broken) > 0:
        for link in broken:
            print "\t%s is BROKEN" % link

if __name__ == "__main__":
    MEDIA_WIKI_URL = 'www.mantidproject.org'

    site = mwclient.Site(MEDIA_WIKI_URL, path='/')
    username = raw_input("Username:")
    passwd = getpass.getpass()
    site.login(username, passwd)

    check_extlinks_on_all(site, "Mantid_Basic_Course")
    check_extlinks_on_all(site, "Introduction_To_Python")
    check_extlinks_on_all(site, "Python_In_Mantid")
    check_extlinks_on_all(site, "Extending_Mantid_With_Python")



