# -*- coding: utf-8 -*-
"""PDF-fill for heating cables."""
# pylama:ignore=W0512

import base64
import os
import re
import sys

from flask import (flash, redirect, render_template, request,
                   send_from_directory, url_for)
from flask.json import jsonify

import forms
import my_exceptions
from norwegian_adresses.address_pymongo import get_address_from_street_name
from flask_login import current_user, login_required
# import schemas
from form_handler import MultiForms
from models import db
from models_credentials import (Company, Customer, Invite, InviteType, Room,
                                RoomItem, RoomTypeInfo, User, user_settings)
from models_product import Manufacturor
from setup_app import app, company_required, json_ok, limiter, manager


@app.route("/cp/")
@login_required
def control_panel():
    """Control-Panel."""
    form = forms.Invite()
    signature = None
    if current_user.signature:
        signature = base64.b64encode(current_user.signature).decode(
            encoding='UTF-8')
    return render_template(
        'control-panel.html', signature=signature, form=form)


@app.route("/cp/company/")
@company_required
def control_panel_company():
    """Control-Panel for viewing users company."""
    if not current_user.company:
        flash('Du er ikke medlem av et firma enda.', 'warning')
        return redirect(url_for('control_panel'))
    form = forms.Invite()
    memmbers = User.query.filter(User.company == current_user.company)
    return render_template(
        'control-panel-company.html', memmbers=memmbers, form=form)


@app.route('/invite/<invite_id>', methods=['GET', 'POST'])
@app.route('/invite/')
# @login_required
def get_invite(invite_id):
    """Route for getting an invite."""
    form = forms.HeatingCableForm()
    invite = Invite.get_invite_from_id(invite_id)
    if not invite:
        flash('Denne invitasjonsnøkkelen er ikke gyldig.', 'warning')
        return redirect(url_for('control_panel'))
    if invite.type == InviteType.create_company:
        return set_company(invite=invite)
    elif invite.type == InviteType.company:
        pass
    if request.method == 'GET':
        return render_template('invite.html', invite=invite, form=form)

    if request.method == 'POST':
        if invite.type == InviteType.company:
            invite.invitee = current_user
            current_user.company = invite.company
            db.session.commit()
            return redirect(url_for('view_form', pane=1))


@app.route('/company/edit', methods=['GET', 'POST'])
@login_required
def set_company():
    """Create or edit a users company."""
    form = forms.CreateCompany()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                current_user.company = Company.update_or_create_all(
                    form, current_user.company)
                db.session.add(current_user)
                db.session.commit()
            except (
                    my_exceptions.LocationException,
                    my_exceptions.DuplicateCompany
            ) as e:
                flash(e.message, 'danger')
                return render_template(
                    'create_company.html', form=form)

            return redirect(url_for('control_panel_company'))
        flash(form.errors, 'danger')
        return render_template(
            'create_company.html', form=form, mode='edit')
    if current_user.company:
        form.name.data = current_user.company.name
        form.org_nr.data = current_user.company.orgnumber
        form.description.data = current_user.company.description
        form.address.address1.data = current_user.company.address.address1
        form.address.address2.data = current_user.company.address.address2
        form.address.post_area.data = current_user.company.address.post_area
        form.address.post_code.data = current_user.company.address.post_code
        form.lat.data = current_user.company.lat
        form.lng.data = current_user.company.lng
        form.phone.data = current_user.company.contact_phone
        form.contact_name.data = current_user.company.contact_name
        form.installer_name.data = current_user.company.installer_name
        form.email.data = current_user.company.contact_email

    return render_template('create_company.html', form=form)


@app.route('/set_sign', methods=['POST'])
@login_required
def save_image():
    """Save an image from a data-string."""

    image_b64 = request.json.get('imageBase64')
    if not image_b64:
        raise my_exceptions.MyBaseException(
            message='Mottok ikke bildedata.',
            status_code=403,
            defcon_level=my_exceptions.DefconLevel.danger)
    if len(image_b64) > 200000:
        raise my_exceptions.MyBaseException(
            message='Bildedataen var for stor.',
            status_code=403,
            defcon_level=my_exceptions.DefconLevel.warning)
    image_data = re.sub('^data:image/.+;base64,', '', image_b64)
    imgdata = base64.b64decode(image_data)
    if current_user.is_authenticated:
        current_user.signature = imgdata
        db.session.commit()
    return jsonify({})


@app.route('/user_files/<path:filename>', methods=['GET'])
@company_required
def download(filename):
    """Serve a file for downloading."""
    directory = os.path.join(app.root_path, app.config['USER_FILES'])
    return send_from_directory(directory=directory, filename=filename)


@limiter.limit("5/10seconds", error_message='Fem per ti sekunder')
@limiter.limit("200/hour", error_message='200 per hour')
@company_required
@app.route('/invite.json', methods=['GET', 'POST'])
def json_invite():
    """Return all invites from current user, or create a new one."""
    form = forms.Invite()
    if form.validate_on_submit():
        try:
            invite = Invite.create(current_user)
            db.session.add(invite)
            db.session.commit()
        except ValueError as e:
            return "{}".format(e), 403
    invites = Invite.get_invites_from_user(current_user).all()
    serialized = ([i.serialize for i in invites])
    return jsonify({'invites': serialized, 'base_url': url_for('get_invite')})


@app.route('/json/v1/static/')
# @limiter.limit("1/second", error_message='Èn per sekund')
@limiter.limit(
    "5/10seconds", error_message='Fem per ti sekunder')
@limiter.limit("200/hour", error_message='200 per hour')
@company_required
def json_static_data():
    """Return a json-object of all products and room-type-info."""
    return jsonify(static_data())


def static_data():
    """Return all static-data. (products, room-type)"""
    manufacturors = Manufacturor.query.all()
    room_types = RoomTypeInfo.query.all()
    return {
        'products': [i.serialize for i in manufacturors],
        'room_type_info': [i.serialize for i in room_types]
    }


@app.route('/form/<customer_id>/<room_id>/<room_item_id>/')
@app.route('/form/<customer_id>/<room_id>/')
@app.route('/form/<customer_id>/')
# @app.route('/form/')
@limiter.limit(
    "5/10seconds", error_message='Fem per ti sekunder')
@company_required
def retrieve_pdf_form(customer_id, room_id=None, room_item_id=None):
    """Create and retrieve all pdf-forms recursively."""
    if room_item_id:
        entity = RoomItem.by_id(room_item_id, current_user)
    elif room_id:
        entity = Room.by_id(room_id, current_user)
    elif customer_id:
        entity = Customer.by_id(customer_id, current_user)
    multi_forms = MultiForms(entity, current_user,
                             stamp=app.config.get('SHOULD_STAMP_PDFS', True))
    pdf_file = multi_forms.file
    if not pdf_file:
        raise my_exceptions.MyBaseException(
            message='Kunne ikke lage skjema. Det har skjedd enn feil.',
            status_code=403,
            defcon_level=my_exceptions.DefconLevel.danger
        )
    return jsonify({
        'file_download': pdf_file
    })


@app.route('/forms.json')
# @limiter.limit("1/second", error_message='Èn per sekund')
@limiter.limit(
    "5/10seconds", error_message='Fem per ti sekunder')
@limiter.limit("200/hour", error_message='200 per hour')
@company_required
def json_user_forms():
    """Return a json-object of all the users forms."""
    result = {'user_forms': [], 'company_forms': []}
    page = request.args.get('page', 1)
    user_forms, user_pages = current_user.\
        get_forms(page=page)
    if current_user and current_user.company:
        company_forms, company_pages = current_user\
            .company\
            .get_forms(
                user=current_user,
                page=page
            )
        if company_forms:
            result['company_forms'] = [
                i.serialize(current_user) for i in company_forms
            ]
            result['company_pages'] = company_pages
    if user_forms:
        result['user_forms'] = [i.serialize(current_user) for i in user_forms]
        result['user_pages'] = user_pages
    return jsonify(result)


@app.route('/json/v1/multi_save', methods=['POST', 'PUT'])
@company_required
def json_multi_save():
    """Save multiple items at once."""
    return_data = {}
    form = forms.MultiSave.from_json(
        request.json, skip_unknown_keys=False)
    if not form.validate_on_submit():
        print(form.errors)
        raise my_exceptions.ValidationErrors(validation_errors=form.errors)
    if form.customer.customer_id.data:
        customer_id = form.customer.customer_id.data
        customer = None
        if customer_id >= 0:
            customer = Customer.by_id(customer_id, current_user)
            if not customer:
                raise my_exceptions.NotACustomer
        customer = Customer.update_or_create(customer, form.customer, current_user)
        if customer:
            return_data['customer'] = {'customer_id': customer.id}
    for heating_cable in form.heating_cables.data:
        room_item = RoomItem.by_id(heating_cable['id'], current_user)
        new_room_item = RoomItem.update_or_create(
            room_item=room_item,
            user=current_user,
            product_id=heating_cable['product_id'],
            room_id=heating_cable['room_id'],
            specs=heating_cable['specs'],)
        if not room_item and new_room_item:
            return_data['heating_cable'] = new_room_item.serialize
    for room in form.rooms.data:
        room_entity = Room.update_or_create(
            room_id=room['id'],
            user=current_user,
            customer_id=room['customer_id'],
            name=room['room_name'],
            outside=room['outside'],
            area=room['area'],
            heated_area=room['heated_area'],
            maxEffect=room['maxEffect'],
            normalEffect=room['normalEffect'],
            curcuit_breaker_size=room['curcuit_breaker_size'],
            installation_depth=room['installation_depth'],
            ground_fault_protection=room['ground_fault_protection'],
            earthed_cable_screen=room['check_earthed']['cable_screen'],
            earthed_chicken_wire=room['check_earthed']['chicken_wire'],
            handed_to_owner=room['handed_to_owner'],
            owner_informed=room['owner_informed'],
            earthed_other=room['check_earthed']['other'],
            max_temp_planning=room['check_max_temp']['planning'],
            max_temp_installation=room['check_max_temp']['installation'],
            max_temp_other=room['check_max_temp']['other'],
            control_system_floor_sensor=room['check_control_system']['floor_sensor'],
            control_system_limit_sensor=room['check_control_system']['limit_sensor'],
            control_system_room_sensor=room['check_control_system']['room_sensor'],
            control_system_designation=room['check_control_system']['designation'],
            control_system_other=room['check_control_system']['other'],
            inside_specs=room['inside_specs'],
            outside_specs=room['outside_specs'],
        )
        if int(room['id']) < 0:
            return_data['room'] = room_entity.serialize

    db.session.commit()
    return jsonify(return_data) if return_data else json_ok()


@app.route('/json/v1/heat/', methods=['DELETE'])
@company_required
def json_heating_cable():
    """Handle a heatining-cable-form."""
    room_item = None
    room_item_id = request.args.get('id') or request.json.get('id')
    if room_item_id:
        room_item = RoomItem.by_id(room_item_id, current_user)
    if not room_item:
        raise my_exceptions.NotARoomItem

    room_item.put_in_archive(current_user)
    return json_ok()


@app.route('/json/v1/room/', methods=['DELETE'])
@company_required
def json_room():
    """Handle a room-object"""
    form = forms.RoomForm.from_json(request.json)
    room_id = form.id.data or request.args.get('id')
    room = None
    if room_id:
        room = Room.by_id(room_id, current_user)
    if not room:
        raise my_exceptions.NotARoom
    if request.method == 'DELETE':
        room.put_in_archive(current_user)
        return json_ok()


@app.route('/json/v1/list/customers/')
@company_required
def json_customer_list():
    """Retrieve a list of all customers relevant to a user."""
    datas = request.json or request.args or {}
    try:
        page = int(datas.get('page', 1))
        per_page = int(datas.get('per_page', 10))
    except ValueError:
        raise my_exceptions.MyBaseException(
            message='Mottok feil side-data. Forventet tall, men fikk {},{}'
            .format(page, per_page),
            status_code=403,
            defcon_level=my_exceptions.DefconLevel.danger
        )
    customers = Company.customer_list_query(current_user.company_id)\
        .order_by(Customer.modified_on_date.desc())\
        .paginate(page, per_page, False)
    return jsonify({
        'pages': customers.pages,
        'page': customers.page,
        'customers': [
            i.serialize_short
            for i in customers.items]
    })


@app.route('/json/v1/customer/', methods=['GET', 'DELETE'])
@company_required
def json_customer():
    """Handle a customer-object"""
    form = forms.CustomerForm.from_json(request.json)
    customer_id = form.customer_id.data or request.args.get('id')
    customer = None
    if customer_id:
        customer = Customer.by_id(customer_id, current_user)

    if request.method == "GET":
        if not customer_id:
            customer = current_user.last_edit
            if not customer:
                raise my_exceptions.NotACustomer(
                    status_code=200,
                    defcon_level=my_exceptions.DefconLevel.default)
        if not customer:
            raise my_exceptions.NotACustomer()
        current_user.last_modified_customer = customer
        db.session.commit()
        return jsonify(customer.serialize)

    if not customer:
        raise my_exceptions.NotACustomer()
    if request.method == 'DELETE':
        customer.put_in_archive(current_user)
        return json_ok()


def user_setting(setting, equal_to):
    """Check if user has a setting equal to."""
    if (
            current_user and
            current_user.settings and
            current_user.settings.get(setting) == equal_to
    ):
        return True
    return False


@app.route('/app')
@company_required
def view_form(pane=0):
    """View for home."""
    # WARNING: NEVER PUT THIS IN PRODUCTION!
    # login_user(User.query.filter(User.id==1).first())
    # Set up some defaults. (retrieve this from the user-config later.)
    if not current_user.signature and not user_setting('disable-tips-signature', True):
        flash('tip-signature')
    heatingForm = forms.HeatingCableForm()
    customerForm = forms.CustomerForm()
    form = forms.CustomerForm()
    roomForm = forms.RoomForm()
    pane = request.args.get('pane', pane)
    try:
        pane = int(pane)
    except ValueError:
        pane = 0
    if not (0 <= pane <= 1):
        pane = 0
    return render_template(
        'main.html',
        heatingForm=heatingForm,
        customerForm=customerForm,
        form=form,
        roomForm=roomForm,
        pane=pane,
        is_app=True)


@login_required
@app.route('/json/v1/user/set_setting/', methods=['POST'])
def set_user_setting():
    """Set a user-setting."""
    if not request.json:
        raise my_exceptions.MyBaseException(
            message='Mottok ikke noe data',
            defcon_level=my_exceptions.DefconLevel.warning,
            status_code=403
        )
    if not current_user.settings:
        current_user.settings = {}
    for key, value in request.json.items():
        if key in user_settings:
            current_user.settings[key] = value
        else:
            db.session.rollback()
            raise my_exceptions.MyBaseException(
                message='Fikk en ugyldig verdi {}'.format(key),
                defcon_level=my_exceptions.DefconLevel.danger,
                status_code=403
            )
    db.session.commit()
    return json_ok()


@app.route('/')
def main():
    """Landing-page-view."""
    if current_user and current_user.is_authenticated and current_user.company:
        return view_form()
    return landing_page()


@app.route('/welcome')
def landing_page():
    """Landing-page-view."""
    return render_template("landing.html")

@app.route('/help')
def help():
    """Helps-view."""
    return render_template("help.html")


@login_required
@limiter.limit("200/minute", error_message='200 per minutt')
@app.route('/address/')
def search_address():
    """Search a partial address (near user)."""
    kwargs = {}
    if current_user.company:
        if current_user.company.lat and current_user.company.lng:
            kwargs['near_geo'] = [
                float(current_user.company.lat),
                float(current_user.company.lng)
            ]
        else:
            kwargs['near_post_code'] = current_user.company.address.post_code
    # Make sure 'post_code' is an int.
    try:
        post_code = request.args.get('p')
        if post_code:
            kwargs['near_post_code'] = int(post_code)
    except ValueError:
        pass
    kwargs['street_name'] = request.args.get('q')
    # Try to get a valid address from search-query
    try:
        results = get_address_from_street_name(**kwargs)
    except ValueError:
        return jsonify(None)
    return jsonify(results)


# hook up extensions to app
if __name__ == "__main__":
    if 'db' in sys.argv:
        manager.run()
    elif 'static' in sys.argv:
        with app.app_context():
            data = static_data()
            import json
            from models import MyJSONEncoder # noqa
            json.JSONEncoder = MyJSONEncoder

            with open('src/data.json', 'w') as fp:
                json.dump(data, fp, cls=MyJSONEncoder, separators=(',', ':'))
    else:
        if app.config['DEBUG'] is True:
            app.run(host='0.0.0.0', port=app.config['PORT'])
