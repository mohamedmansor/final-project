from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from flask import Flask, render_template, request
from flask import redirect, url_for, jsonify, flash
app = Flask(__name__)


# DB Connection
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# ---------------End OF Fake Data------------
# Restaurant URLS


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html',
                           restaurants=restaurants)


@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        restaurantToCreate = Restaurant(name=request.form['name'])
        session.add(restaurantToCreate)
        session.commit()
        flash("A new Restaurant has been Created")
        return redirect(url_for('newRestaurant'))
    else:
        return render_template('newRestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    edit_restaurant = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            edit_restaurant.name = request.form['name']
        session.add(edit_restaurant)
        session.commit()
        flash("Restaurant has been edited")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html',
                               restaurant_id=restaurant_id,
                               restaurant=edit_restaurant)


@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurantToDelete = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            restaurantToDelete = request.form['name']
        session.delete(restaurantToDelete)
        session.commit()
        flash("Restaurant has been deleted")
        return redirect(url_for('showRestaurants'),
                        restaurant_id=restaurant_id)
    else:
        return render_template('deleteRestaurant.html',
                               restaurant=restaurantToDelete)
# Adding JSON


@app.route('/restaurants/JSON')
def restaurantJSON():
    restaurantsItems = session.query(Restaurant).all()
    return jsonify(Restaurant=[i.serialize for i in restaurantsItems])


@app.route('/restaurants/<int:restaurant_id>/JSON')
def restaurantIdJSON(restaurant_id):
    restaurantsItems = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    return jsonify(Restaurant=restaurantsItems.serialize)

# Menu URLS


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJson(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)


@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(id=restaurant_id)
    return render_template('menu.html',
                           items=items, restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        itemToCreate = MenuItem(name=request.form['name'],
                                description=request.form['description'],
                                price=request.form['price'],
                                course=request.form['course'])
        session.add(itemToCreate)
        session.commit()
        flash("A new Menu has been Created")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newMenuItem.html',
                               restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    itemToEdit = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            itemToEdit.name = request.form['name']
        if request.form['description']:
            itemToEdit.description = request.form['name']
        if request.form['price']:
            itemToEdit.price = request.form['price']
        if request.form['course']:
            itemToEdit.course = request.form['course']
            session.add(itemToEdit)
            session.commit()
            flash("The Item has been Edited")
            return redirect(url_for('showRestaurants'),
                            restaurant_id=restaurant_id)
    else:
        return render_template('editMenuItem.html',
                               restaurant_id=restaurant_id,
                               menu_id=menu_id,
                               item=itemToEdit)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("The Item has been deleted")
        return redirect(url_for('showRestaurants',
                                restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html',
                               restaurant_id=restaurant_id,
                               menu_id=menu_id,
                               item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'final_project'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
