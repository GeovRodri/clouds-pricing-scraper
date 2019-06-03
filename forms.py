from wtforms import Form, FieldList, StringField, validators, FormField, Field, IntegerField


class CloudSelectForm(Form):
    aws = FieldList(StringField(validators=[validators.DataRequired()]))
    oracle = FieldList(StringField(validators=[validators.DataRequired()]))
    alibaba = FieldList(StringField(validators=[validators.DataRequired()]))
    azure = FieldList(StringField(validators=[validators.DataRequired()]))
    google = FieldList(StringField(validators=[validators.DataRequired()]))


class CloudFilter(Form):
    field = StringField(validators=[validators.DataRequired()])
    comparator = StringField(validators=[validators.DataRequired()])
    value = Field(validators=[validators.DataRequired()])


class FindCloudsForm(Form):
    select = FormField(CloudSelectForm)
    labels = FieldList(StringField(validators=[validators.DataRequired()]))
    filters = FieldList(FormField(CloudFilter))
    limit = IntegerField()
