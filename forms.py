from wtforms import Form, FieldList, StringField, validators, FormField, Field


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


class CloudFiltersForm(Form):
    aws = FieldList(FormField(CloudFilter))
    oracle = FieldList(FormField(CloudFilter))
    alibaba = FieldList(FormField(CloudFilter))
    azure = FieldList(FormField(CloudFilter))
    google = FieldList(FormField(CloudFilter))


class FindCloudsForm(Form):
    select = FormField(CloudSelectForm)
    filters = FormField(CloudFiltersForm)
