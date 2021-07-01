from market import app, db, bcrypt
from flask import render_template, url_for, redirect, flash, request
from market.models import Item
from market.forms import RegistrationForm, LoginForm, PurchaseItemForm, SellItemForm
from market.models import User, Item
from flask_login import login_user, logout_user, login_required, current_user



@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', title='Home Page')


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market():
	purchase_form = PurchaseItemForm()
	selling_form = SellItemForm()

	if request.method == 'POST':
		# purchase logic
		purchsed_item = request.form.get('purchased_item')
		p_item_object = Item.query.filter_by(name=purchsed_item).first()

		if p_item_object:
			if current_user.can_purchase(p_item_object):
				p_item_object.buy(current_user)
				flash("you have successfully purchased this item", 'success')
			else:
				flash(f"Unfortunately you don't have enough money to purchase {p_item_object.name}",  'warning')

		# selling logic
		sold_item = request.form.get('sold_item')
		s_item_object = Item.query.filter_by(name=sold_item).first()

		if s_item_object:
			if current_user.can_sell(s_item_object):
				s_item_object.sell(current_user)
				flash(f"you sold {s_item_object.name} back to market", 'success')
			else:
				flash(f"something went wrong with selling {s_item_object.name}", 'danger')

		return redirect(url_for('market'))


	if request.method == 'GET':
		items = Item.query.filter_by(owner=None)
		owned_items = Item.query.filter_by(owner=current_user.id)
		return render_template('market.html', title='Market', items=items, owned_items=owned_items,
							    purchase_form=purchase_form, selling_form=selling_form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user_to_create = User(username=form.username.data, 
							  email_address=form.email_address.data, 
							  password=hash_password)
		db.session.add(user_to_create)
		db.session.commit()
		flash(f'your account has been created successfully', 'success')
		login_user(user_to_create)
		return redirect(url_for('market'))
	else:
		return render_template('register.html', form=form, title='register')



@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		attempted_user = User.query.filter_by(email_address=form.email_address.data).first()
		if attempted_user and attempted_user.check_password(attempted_password=form.password.data):
			login_user(attempted_user)
			flash('login successful', 'success')

			return redirect(url_for('market'))
		else:
			flash('incorrect email address or password', 'danger')
	return render_template('login.html', form=form, title='login')

@app.route('/logout')
def logout():
	logout_user()
	flash('you have been logged out', 'info')
	return redirect(url_for('home'))