from globals import *
from routes.helpers import *
from flask import Blueprint, request, jsonify, render_template, redirect

app = Blueprint('custom_location', __name__, template_folder='templates')


@app.route('/custom-location/set', methods=['POST'])
@auth_required
def set_custom_location_form(userid):
	"""
	Handle form submission for setting custom location
	"""
	if not verify_csrf(request.form['csrf']):
		return 'Please refresh and try again', 401
	
	if 'location' not in request.form or not request.form['location'].strip():
		return 'Location is required', 400
	
	location = request.form['location'].strip()
	
	if len(location) > 26:
		return 'Location too long (max 26 characters)', 400
	
	try:
		expiration = int(request.form.get('expiration', 3600))
		if expiration <= 0 or expiration > 86400:  # Max 24 hours
			return 'Invalid expiration time (must be 1-86400 seconds)', 400
	except ValueError:
		return 'Invalid expiration time format', 400
	
	set_user_defined_location(userid['userid'], location, expiration)
	
	return redirect('/custom-location/', 303)


@app.route('/custom-location/remove', methods=['POST'])
@auth_required
def remove_custom_location_form(userid):
	"""
	Handle form submission for removing custom location
	"""
	if not verify_csrf(request.form['csrf']):
		return 'Please refresh and try again', 401
	
	key = f"USER_DEFINED_LOCATION>{userid['userid']}"
	r.delete(key)
	
	return redirect('/custom-location/', 303)

