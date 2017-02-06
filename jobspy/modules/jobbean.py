from data_handler import * 

# connect database
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'baidu123',
    'database': 'test'
}
Database.connect(**db_config)

# define model
class JobModel(Model):
    db_table = 'jobinfo'  # point table name
    id = Field()
    title = Field()
    url = Field()
    email = Field()
    content = Field()
    time = Field()
    type = Field()
    jobtag = Field()
    tags = Field()

class TagModel(Model):
    db_table = 'tag'
    id = Field()
    tag = Field()

class JobCrossTagModel(Model):
    db_table = 'jobtag'
    url = Field()
    tagid = Field()
    type = Field()
    time = Field()

class SimDup1(Model):
    db_table = 'simdup1'
    hashpart = Field()
    hash = Field()
    url = Field()
    time = Field()
    date = Field()

class SimDup2(Model):
    db_table = 'simdup2'
    hashpart = Field()
    hash = Field()
    url = Field()
    time = Field()
    date = Field()

class SimDup3(Model):
    db_table = 'simdup3'
    hashpart = Field()
    hash = Field()
    url = Field()
    time = Field()
    date = Field()

class SimDup4(Model):
    db_table = 'simdup4'
    hashpart = Field()
    hash = Field()
    url = Field()
    time = Field()
    date = Field()
