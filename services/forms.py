from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, TextAreaField, SelectField, HiddenField, IntegerField, validators, FormField, FieldList, BooleanField, DateField
from wtforms.fields.html5 import DateField as htmldate
from flask_wtf.file import FileField, FileRequired, FileAllowed

class CustomerLogin(FlaskForm):
    email = StringField('email', validators=[validators.InputRequired(), validators.Email()])
    password = PasswordField('password', validators=[validators.InputRequired()])

class ForgotPassword(FlaskForm):
    email = StringField('email', validators=[validators.InputRequired(), validators.Email()])

class UpdatePassword(FlaskForm):
    password = PasswordField('password', validators=[validators.InputRequired()])

class CreateCustomer(FlaskForm):
    email = StringField('email', validators=[validators.InputRequired(), validators.Email()])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('confirm', validators=[validators.DataRequired()])

class Profile(FlaskForm):
    first_name = StringField('first_name', validators=[validators.InputRequired()])
    last_name = StringField('last_name', validators=[validators.InputRequired()])
    company_name = StringField('company_name', validators=[validators.InputRequired()])
    revenue = StringField('revenue', validators=[validators.InputRequired()])
    zip = StringField('zip', validators=[validators.Length(max=5, min=5)])
    stage = HiddenField('stage')
    employees = StringField('employees')
    website = StringField('website')

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
    rev_channel_freeform = TextAreaField('rev_channel_freeform')
    storefront_perc = StringField('storefront_perc')
    direct_perc = StringField('direct_perc')
    online_perc = StringField('online_perc')
    tradeshows_perc = StringField('tradeshows_perc')
    other_perc = StringField('other_perc')

class Audience(FlaskForm):
    persona_name = StringField('persona_name')
    gender = StringField('gender')
    location = StringField('location')
    company_size = StringField('company_size')
    formality = StringField('formality')
    buying_for = StringField('buying_for')
    tech_savvy = StringField('tech_savvy')
    decision_making = StringField('decision_making')
    details = StringField('details')
    motive = StringField('motive')
    why = StringField('why')
    before_freeform = TextAreaField('before_freeform')
    after_freeform = TextAreaField('after_freeform')
    age_group_1 = StringField('age_group_1')
    age_group_2 = StringField('age_group_2')
    age_group_3 = StringField('age_group_3')
    age_group_4 = StringField('age_group_4')
    age_group_5 = StringField('age_group_5')
    age_group_6 = StringField('age_group_6')
    age_group_7 = StringField('age_group_7')
    before_1 = StringField('before_1')
    before_2 = StringField('before_2')
    before_3 = StringField('before_3')
    before_4 = StringField('before_4')
    before_5 = StringField('before_5')
    before_6 = StringField('before_6')
    before_7 = StringField('before_7')
    before_8 = StringField('before_8')
    before_9 = StringField('before_9')
    before_10 = StringField('before_10')
    after_1 = StringField('after_1')
    after_2 = StringField('after_2')
    after_3 = StringField('after_3')
    after_4 = StringField('after_4')
    after_5 = StringField('after_5')
    after_6 = StringField('after_6')
    after_7 = StringField('after_7')
    after_8 = StringField('after_8')
    after_9 = StringField('after_9')
    after_10 = StringField('after_10')



class ProductList(FlaskForm):
    name = StringField('Name')
    category = StringField('Category')
    cogs = StringField('COGS')
    sales_price = StringField('Sales Price')
    price_model = SelectField('Price Model', choices=[('monthly recurring', 'monthly recurring'), ('annual recurring', 'annual recurring'), ('one-time payment', 'one-time payment')])
    qty_sold = StringField('Qty Sold Last 12 Months')
    est_unique_buyers = StringField('Est. Unique Buyers')


class Product(FlaskForm):
    gen_description = TextAreaField('gen_description')
    quantity = IntegerField('quantity')
    link = StringField('link')
    segment_1 = StringField('segment_1')
    segment_2 = StringField('segment_2')
    segment_3 = StringField('segment_3')
    segment_4 = StringField('segment_4')
    segment_5 = StringField('segment_5')
    segment_6 = StringField('segment_6')
    segment_7 = StringField('segment_7')
    segment_8 = StringField('segment_8')
    segment_9 = StringField('segment_9')
    segment_10 = StringField('segment_10')
    source_1 = StringField('source_1')
    source_2 = StringField('source_2')
    source_3 = StringField('source_3')
    source_4 = StringField('source_4')
    source_5 = StringField('source_5')
    source_freeform = TextAreaField('source_freeform')
    product = FieldList(FormField(ProductList), min_entries=1)

class Product_2(FlaskForm):
    complexity = StringField('complexity')
    price = StringField('price')
    frequency_of_use = StringField('frequency_of_use')
    frequency_of_purchase = StringField('frequency_of_purchase')
    value_prop_1 = StringField('value_prop_1')
    value_prop_2 = StringField('value_prop_2')
    value_prop_3 = StringField('value_prop_3')
    value_prop_4 = StringField('value_prop_4')
    value_prop_5 = StringField('value_prop_5')
    warranties_or_guarantee = StringField('warranties_or_guarantee')
    warranty_guarantee_freeform = TextAreaField('warranty_guarantee_freeform', id="wogf")
    num_skus = StringField('num_skus')
    level_of_customization = StringField('level_of_customization')

class stage_grouping_left (FlaskForm):
    input_1 = StringField('input', id="awareness_test")
    input_2 = StringField('input')
    input_3 = StringField('input')
    input_4 = StringField('input')
    input_5 = StringField('input')
    input_6 = StringField('input')

class stage_grouping_right (FlaskForm):
    input_7 = StringField('input', id="awareness_test")
    input_8 = StringField('input')
    input_9 = StringField('input')
    input_10 = StringField('input')
    input_11 = StringField('input')
    input_12 = StringField('input')

class SalesCycle(FlaskForm):
    awareness_left = FormField(stage_grouping_left)
    awareness_right = FormField(stage_grouping_right)
    evaluation_left = FormField(stage_grouping_left)
    evaluation_right = FormField(stage_grouping_right)
    conversion_left = FormField(stage_grouping_left)
    conversion_right = FormField(stage_grouping_right)
    retention_left = FormField(stage_grouping_left)
    retention_right = FormField(stage_grouping_right)
    referral_left = FormField(stage_grouping_left)
    referral_right = FormField(stage_grouping_right)


class Goals(FlaskForm):
    goal = StringField('goal')
    current_avg = StringField('current_avg')
    target_avg = StringField('target_avg')
    timeframe = StringField('timeframe')

class History(FlaskForm):
    facebook = HiddenField('facebook')
    google = HiddenField('google')
    bing = HiddenField('bing')
    twitter = HiddenField('twitter')
    instagram = HiddenField('instagram')
    yelp = HiddenField('yelp')
    linkedin = HiddenField('linkedin')
    amazon = HiddenField('amazon')
    snapchat = HiddenField('snapchat')
    youtube = HiddenField('youtube')
    none = HiddenField('none')
    digital_spend = SelectField('digital_spend', choices=[('n/a', 'n/a'),
                                                          ('<$500/month', '<$500/month'),
                                                          ('$500-$1,000/month', '$500-$1,000/month'),
                                                          ('$1,000-$2,000/month', '$1,000-$2,000/month'),
                                                          ('$2,000-$5,000/month', '$2,000-$5,000/month'),
                                                          ('$5,000-$10,000/month', '$5,000-$10,000/month'),
                                                          ('$10,000-$20,000/month', '$10,000-$20,000/month'),
                                                          ('$20,000-$50,000/month', '$20,000-$50,000/month'),
                                                          ('$50,000-$100,000/month', '$50,000-$100,000/month'),
                                                          ('$100,000+', '$100,000+'),
                                                          ], default='n/a')

class Platforms(FlaskForm):
    test = HiddenField('test')

class Past(FlaskForm):
    freeform = TextAreaField('freeform')



# admin forms

class AdminLogin(FlaskForm):
    email = StringField('email', validators=[validators.InputRequired(), validators.Email()])
    password = PasswordField('password', validators=[validators.InputRequired()])

class AddRep(FlaskForm):
    rep_name = BooleanField()

class TaskForm(FlaskForm):
    title = StringField('task title', validators=[validators.InputRequired()])

class CSVForm(FlaskForm):
    start_date = htmldate('start date', validators=[validators.InputRequired()])
    end_date = htmldate('end date', validators=[validators.InputRequired()])
    csv = FileField('csv', validators=[FileRequired(), FileAllowed(['csv'], 'Please make sure the csv format is correct!')])

class ABForm(FlaskForm):
    start_date = htmldate('start date', validators=[validators.InputRequired()])
    end_date = htmldate('end date', validators=[validators.InputRequired()])
    csv = FileField('csv', validators=[FileRequired(), FileAllowed(['csv'], 'Please make sure the csv format is correct!')])
    
class InsightForm(FlaskForm):
    body = TextAreaField('body', validators=[validators.InputRequired()])

class TagForm(FlaskForm):
    search = StringField('search')
    #Business model
    any_model = BooleanField('any')
    b2b = BooleanField('b2b')
    b2c = BooleanField('b2c')
    c2c = BooleanField('c2c')
    #Challenge
    easy = BooleanField('Easy')
    moderate = BooleanField('Moderate')
    difficult = BooleanField('Difficult')
    tbd = BooleanField('TBD')
    #Sales Cycle
    awareness = BooleanField('Awareness')
    evaluation = BooleanField('Evaluation')
    conversion = BooleanField('Conversion')
    retention = BooleanField('Retention')
    referral = BooleanField('Referral')
    #Goals
    any_goal = BooleanField('any_goal')
    revenue = BooleanField('revenue')
    cac = BooleanField('cac')
    users = BooleanField('users')
    leads = BooleanField('leads')
    other = BooleanField('other')
    #Key metric
    any_metrics = BooleanField('any_metrics')
    visitors = BooleanField('visitors')
    sales = BooleanField('sales')
    clicks = BooleanField('clicks')
    downloads = BooleanField('downloads')
    email_signup = BooleanField('email_signup')
    registration = BooleanField('registration')
    views = BooleanField('views')
    shares = BooleanField('shares')
    engagement = BooleanField('engagement')
    leads = BooleanField('leads')
    other = BooleanField('other')
    #Company Type
    any_type = BooleanField('any_type')
    digital_product = BooleanField('digital_product')
    tangible_product = BooleanField('tangible_product')
    saas = BooleanField('saas')
    ecommerce = BooleanField('ecommerce')
    affiliate_commission = BooleanField('affiliate_commission')
    media = BooleanField('media')
    professional_services = BooleanField('professional_services')
    manual_services = BooleanField('manual_services')
    franchise = BooleanField('franchise')
    brick_and_mortar = BooleanField('brick_and_mortar')
    food_and_beverage = BooleanField('food_and_beverage')
    #4 P's
    na = BooleanField('na')
    pricing = BooleanField('pricing')
    product = BooleanField('product')
    place = BooleanField('place')
    promotion = BooleanField('promotion')
    #Other Tags
    ab_test = BooleanField('')
    ad_campaigns = BooleanField('')
    branding = BooleanField('')
    copy = BooleanField('')
    cta = BooleanField('')
    customer_experience = BooleanField('')
    email = BooleanField('')
    facebook = BooleanField('')
    instagram = BooleanField('')
    landing_page = BooleanField('')
    lead_gen = BooleanField('')
    linkedin = BooleanField('')
    links = BooleanField('')
    pinterest = BooleanField('')
    pricing = BooleanField('')
    product = BooleanField('')
    promotion = BooleanField('')
    public_awareness = BooleanField('')
    retargeting = BooleanField('')
    reviews = BooleanField('')
    segmentation = BooleanField('')
    seo = BooleanField('')
    social = BooleanField('')
    twitter = BooleanField('')
    ui = BooleanField('')
    website = BooleanField('')
