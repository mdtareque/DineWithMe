# -*- coding: utf-8 -*-


db.define_table('profile'
                ,Field('id', 'reference auth_user')
                ,Field('name', 'string')
                ,Field('dob', 'date')
                ,Field('profession', 'string')
                ,Field('gender', 'string')
                ,Field('city', 'string')
                ,auth.signature)
db.profile.gender.requires=IS_IN_SET(('Male','Female'))
db.profile.profession.requires=IS_IN_SET(('Student', 'Professor', 'Engineer', 'Entrepreneur', 'BusinessMan', 'Traveller', 'Author', 'Other'))

db.define_table('interestlist' ,Field('name', 'string'))

db.define_table('interests'
               ,Field('userid', 'integer')
               ,Field('iid', 'reference interestlist')
               )

db.define_table('requests'
                ,Field('user_id','reference auth_user' )
                ,Field('place', 'string')
                ,Field('rtime', 'datetime')
                ,Field('foodtype', 'string')
                ,Field('expiry', 'datetime')
               )

db.define_table('messages'
                ,Field('ts', 'datetime')
                ,Field('txt' , 'string')
                ,Field('rid', 'reference messages')
                )

db.define_table('chat'
               ,Field('rid', 'reference requests')
               ,Field('user_id', 'integer')
               )
