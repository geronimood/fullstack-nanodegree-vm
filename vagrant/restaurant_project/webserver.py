from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += restaurant_list()
                output += "<p><a href = '/new'>Make an new restaurant!</a></p>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Make a new restaurant!</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/new'><h2>Pls enter name of new restaurant</h2><input name='new_message' type='text'><input type='submit' value='submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                path_part = self.path.split()
                split_path = path_part[0].split('/')
                global res_id_edit
                res_id_edit = split_path[1]
                res_name = lookup_restaurant(res_id_edit)

                output = ""
                output += "<html><body>"
                output += "<h1>%s</h1>" % res_name
                output += "<form method='POST' enctype='multipart/form-data' action='/edit'><h2>Pls enter new name of the restaurant</h2><input name='edit_message' type='text'><input type='submit' value='Rename'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                path_part = self.path.split()
                split_path = path_part[0].split('/')
                global res_id_del
                res_id_del = split_path[1]
                res_name = lookup_restaurant(res_id_del)

                output = ""
                output += "<html><body>"
                output += "<h1>Pls confirm to delete</h1>"
                output += "<h1>%s</h1>" % res_name
                output += "<form method='POST' enctype='multipart/form-data' action='/delete'><input name='delete_message' input type='submit' value='Confirm!'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except:
            self.send_error(404, "File Not Found %s" % self.path)


    def do_POST(self):
        try:

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                content_new = fields.get('new_message')
                content_edit = fields.get('edit_message')
                content_delete = fields.get('delete_message')

            if self.path.endswith("/new"):
                if content_new[0] != "":
                    new_restaurant(content_new[0])
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', 'restaurants')
                    self.end_headers()

            if self.path.endswith("/edit"):
                if content_edit[0] != "":
                    edit_restaurant(res_id_edit, content_edit[0])
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', 'restaurants')
                    self.end_headers()

            if self.path.endswith("/delete"):
                if content_delete[0] != "":
                    delete_restaurant(res_id_del)
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', 'restaurants')
                    self.end_headers()

        except:
            pass

def DB_connect():
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind = engine)
    global session
    session = DBSession()

def restaurant_list():
    DB_connect()
    r_list = session.query(Restaurant).all()
    r_list_str = ""
    for restaurant in r_list:
        link_edit = '/' + str(restaurant.id) + '/edit'
        link_delete = '/' + str(restaurant.id) + '/delete'
        r_list_str += "<p>" + str(restaurant.name)
        r_list_str += "<br><a href =" + link_edit + ">Edit</a><br>"
        r_list_str += "<a href =" + link_delete + ">Delete</a></p>"

    return r_list_str

def new_restaurant(user_input):
    DB_connect()
    new_res = Restaurant(name = user_input)
    session.add(new_res)
    session.commit()

def edit_restaurant(res_id, new_name):
    DB_connect()
    edit_res = session.query(Restaurant).filter_by(id = res_id).one()
    edit_res.name = new_name
    session.add(edit_res)
    session.commit()

def delete_restaurant(res_id):
    DB_connect()
    delete_res = session.query(Restaurant).filter_by(id = res_id).one()
    session.delete(delete_res)
    session.commit()

def lookup_restaurant(res_id):
    DB_connect()
    res = session.query(Restaurant).filter_by(id = res_id).one()
    res_name = res.name
    return res_name

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Webserver Running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

if __name__ == '__main__':
    main()
