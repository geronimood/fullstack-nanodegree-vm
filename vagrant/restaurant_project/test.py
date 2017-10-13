from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

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
        r_list_str += str(restaurant.name) + '\n'

    print r_list_str

def new_restaurant(user_input):
    DB_connect()
    new_res = Restaurant(name = user_input)
    session.add(new_res)
    session.commit()

def rename_restaurant(res_id, new_name):
    DB_connect()
    rename_res = session.query(Restaurant).filter_by(id = res_id).one()
    rename_res.name = new_name
    session.add(rename_res)
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

new_restaurant("Test Restaurant")
#rename_restaurant(13, "Renamed Restaurant")
#delete_restaurant(12)
restaurant_list()

#DB_connect()
#print session.query(Restaurant.id).all()

#print lookup_restaurant(1)
