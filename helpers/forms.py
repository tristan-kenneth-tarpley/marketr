from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, HiddenField, IntegerField, validators

class Profile(FlaskForm):
    first_name = StringField('first_name', validators=[validators.InputRequired()])
    last_name = StringField('last_name', validators=[validators.InputRequired()])
    company_name = StringField('company_name')
    revenue = IntegerField('revenue', validators=[validators.InputRequired()])
    zip = StringField('zip', validators=[validators.Length(max=5, min=5)])
    stage = HiddenField('stage')
    employees = IntegerField('employees')

class Competitors(FlaskForm):
    industry = StringField('industry', validators=[validators.InputRequired()])
    comp_1_name = StringField('comp_1_name', validators=[validators.InputRequired()])
    comp_1_website = StringField('comp_1_website', validators=[validators.InputRequired()])
    comp_2_name = StringField('comp_2_name', validators=[validators.InputRequired()])
    comp_2_website = StringField('comp_2_website', validators=[validators.InputRequired()])
    comp_1_type = HiddenField('comp_1_type', validators=[validators.InputRequired()])
    comp_2_type = HiddenField('comp_2_type', validators=[validators.InputRequired()])

class Company(FlaskForm):
    selling_to = HiddenField('selling_to')
    biz_model = HiddenField('biz_model', validators=[validators.InputRequired()])
    rev_channel_freeform = StringField('rev_channel_freeform')
    storefront_perc = HiddenField('storefront_perc')
    direct_perc = HiddenField('direct_perc')
    online_perc = HiddenField('online_perc')
    tradeshows_perc = HiddenField('tradeshows_perc')
    other_perc = HiddenField('other_perc')


