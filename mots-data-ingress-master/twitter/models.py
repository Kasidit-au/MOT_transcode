from peewee import *

database = MySQLDatabase('mots-dev', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': 'mots-mariadb.mariadb.database.azure.com', 'port': 3306, 'user': 'xphys@mots-mariadb', 'password': 'ItsInternet'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class AssignmentStatus(BaseModel):
    asg_status_id = AutoField()
    detail = CharField(null=True)
    status_name = CharField(null=True)

    class Meta:
        table_name = 'assignment_status'

class UserPermission(BaseModel):
    permission_id = AutoField()
    permission_name = CharField(null=True)

    class Meta:
        table_name = 'user_permission'

class User(BaseModel):
    firstname = CharField(null=True)
    lastname = CharField(null=True)
    password = CharField(null=True)
    permission = ForeignKeyField(column_name='permission_id', field='permission_id', model=UserPermission, null=True)
    user_id = AutoField()
    user_name = CharField(null=True)

    class Meta:
        table_name = 'user'

class MasterSource(BaseModel):
    source_id = AutoField()
    source_name = CharField(null=True)

    class Meta:
        table_name = 'master_source'

class Assignment(BaseModel):
    asg_id = AutoField()
    asg_status = ForeignKeyField(column_name='asg_status_id', constraints=[SQL("DEFAULT 0")], field='asg_status_id', model=AssignmentStatus)
    assign_to_permission = ForeignKeyField(column_name='assign_to_permission_id', constraints=[SQL("DEFAULT 1")], field='permission_id', model=UserPermission)
    comment_brief = TextField(null=True)
    comment_brief_datetime = DateTimeField(null=True)
    comment_brief_user_id = IntegerField(null=True)
    detail_brief = TextField(null=True)
    detail_brief_datetime = DateTimeField(null=True)
    detail_brief_user = ForeignKeyField(column_name='detail_brief_user_id', field='user_id', model=User, null=True)
    is_active = IntegerField(constraints=[SQL("DEFAULT 1")])
    news_datetime = DateTimeField(null=True)
    news_detail = CharField(null=True)
    news_link = CharField(null=True)
    news_name = CharField(null=True)
    news_ref = CharField(null=True)
    news_source = ForeignKeyField(column_name='news_source_id', field='source_id', model=MasterSource, null=True)
    news_sync_datetime = DateTimeField(null=True)
    news_total_comment = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    news_total_view = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'assignment'

class MasterTag(BaseModel):
    danger_level = IntegerField(null=True)
    is_active = IntegerField(null=True)
    tag_id = AutoField()
    tag_name = CharField(null=True)

    class Meta:
        table_name = 'master_tag'

class AssignmentTag(BaseModel):
    asg = ForeignKeyField(column_name='asg_id', field='asg_id', model=Assignment, null=True)
    asg_tag_id = AutoField()
    create_datetime = DateTimeField(null=True)
    is_active = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    is_system = CharField(null=True)
    tag = ForeignKeyField(column_name='tag_id', field='tag_id', model=MasterTag, null=True)
    update_datetime = DateTimeField(null=True)
    user = ForeignKeyField(column_name='user_id', field='user_id', model=User, null=True)

    class Meta:
        table_name = 'assignment_tag'

class AssignmentToLog(BaseModel):
    asg = ForeignKeyField(column_name='asg_id', field='asg_id', model=Assignment, null=True)
    asg_to_id = AutoField()
    create_datetime = DateTimeField()
    due_datetime = DateTimeField(null=True)
    is_active = IntegerField(constraints=[SQL("DEFAULT 1")])
    is_finish = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_over_duedate = IntegerField(constraints=[SQL("DEFAULT 0")])
    permission_id = IntegerField(constraints=[SQL("DEFAULT 1")])

    class Meta:
        table_name = 'assignment_to_log'

class MasterKeyword(BaseModel):
    is_active = IntegerField(null=True)
    keyword_id = AutoField()
    keyword_name = CharField(null=True)
    tag_id = IntegerField(null=True)

    class Meta:
        table_name = 'master_keyword'

class Reply(BaseModel):
    asg = ForeignKeyField(column_name='asg_id', field='asg_id', model=Assignment, null=True)
    create_datetime = DateTimeField(null=True)
    is_active = IntegerField(null=True)
    msg = CharField(null=True)
    reply_id = AutoField()
    update_datetime = DateTimeField(null=True)
    user = ForeignKeyField(column_name='user_id', field='user_id', model=User, null=True)

    class Meta:
        table_name = 'reply'

class ReplyFile(BaseModel):
    create_datetime = DateTimeField(null=True)
    file_name = CharField(null=True)
    file_path = CharField(null=True)
    is_active = IntegerField(null=True)
    reply_file_id = AutoField()
    reply = ForeignKeyField(column_name='reply_id', field='reply_id', model=Reply, null=True)
    update_datetime = DateTimeField(null=True)

    class Meta:
        table_name = 'reply_file'

class ReplyImg(BaseModel):
    create_datetime = DateTimeField(null=True)
    img_name = CharField(null=True)
    img_path = CharField(null=True)
    is_active = IntegerField(null=True)
    reply = ForeignKeyField(column_name='reply_id', field='reply_id', model=Reply, null=True)
    reply_img_id = AutoField()
    update_datetime = DateTimeField(null=True)

    class Meta:
        table_name = 'reply_img'

class ReplyLink(BaseModel):
    create_datetime = DateTimeField(null=True)
    detail = CharField(null=True)
    is_active = IntegerField(null=True)
    link_name = CharField(null=True)
    link_url = CharField(null=True)
    reply = ForeignKeyField(column_name='reply_id', field='reply_id', model=Reply, null=True)
    reply_link_id = AutoField()
    update_datetime = DateTimeField(null=True)

    class Meta:
        table_name = 'reply_link'

class ReplyVdo(BaseModel):
    create_datetime = DateTimeField(null=True)
    is_active = IntegerField(null=True)
    reply = ForeignKeyField(column_name='reply_id', field='reply_id', model=Reply, null=True)
    reply_vdo_id = AutoField()
    update_datetime = DateTimeField(null=True)
    vdo_name = CharField(null=True)
    vdo_path = CharField(null=True)

    class Meta:
        table_name = 'reply_vdo'

class ReportTagCount(BaseModel):
    array_news_id = CharField(null=True)
    count_news = IntegerField(null=True)
    news_sync_date = DateField(null=True)
    tag_count_id = AutoField()
    tag_id = IntegerField(null=True)

    class Meta:
        table_name = 'report_tag_count'

class UserFavTag(BaseModel):
    create_datetime = DateTimeField(null=True)
    is_active = IntegerField(null=True)
    tag_id = IntegerField(null=True)
    update_datetime = DateTimeField(null=True)
    user_fav_tag_id = AutoField()
    user_id = IntegerField(null=True)

    class Meta:
        table_name = 'user_fav_tag'

