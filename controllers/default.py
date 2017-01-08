# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

#@auth.requires_login()
def profile():
    pr = db(db.profile.id == auth.user_id).select() #profilerow
    profileyes = False
    if len(pr) >0:
        profileyes = True
        pr = pr[0]
        pinterest = db(db.interests.userid == auth.user_id and db.interests.iid == db.interestlist.id).select(db.interestlist.name)
        print pinterest
    profileForm = SQLFORM(db.profile).process()
    return locals()

def interest0():
    options=[  str(x) for x in range(10)]
    #https://groups.google.com/forum/#!topic/web2py/FG1CZJ9X-j8
    form=FORM(SELECT(*options,_name='test',_multiple='multiple'),INPUT (_type='submit', url=''))
    if form.accepts(request,session):
        print request.vars
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)

def interest():
    oldInt = db(db.interests.userid == auth.user_id and db.interests.iid == db.interestlist.id).select(db.interestlist.name)
    iis = db(db.interestlist).select()
    rev = {}
    oldids = []
    for i in iis:
        rev[i['name']] = i['id']
        oldids.append(i['id'])
    options=[  str(x['name']) for x in iis]
    # todo : http://stackoverflow.com/questions/19999852/how-to-preselect-options-in-select-helper-in-web2py
    # pre select old interest
    form=FORM(SELECT(options,_name='interestform',_multiple='multiple',_size=len(iis)),INPUT (_type='submit'))
    if form.accepts(request,session):
        print request.vars.interestform
        response.flash = 'form accepted'
        for j in request.vars.interestform:
#            try:
                oldInt2 = db(db.interests.userid == auth.user_id and db.interests.iid == db.interestlist.id).select(db.interestlist.name)
                oldIntList = []
                for i in oldInt2:
                    oldIntList.append(i['name'])
                if j not in oldIntList:
                    db.interests.insert(userid=auth.user_id, iid=rev[j])
#                else: print 'duplicate entry'
#            except:
#                print 'exception while adding interest, possible dup'
#                pass
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return locals()
    #print iis[0]
    #form = SQLFORM(db.interests).process()
    #return locals()


    
def add_interest():
    print request.args
    print request.vars
    return locals()


def find():
    print request.vars # time , place, foodtype
    
    import datetime 
    print request.now, datetime.datetime.now()
    print datetime.datetime.now() + datetime.timedelta(minutes=30)
    today = datetime.date.today()
    inputtime = request.vars.time.split(':')
    hh, mm = int(inputtime[0]), int(inputtime[1])
    searchTime = datetime.time(hh, mm)
    print searchTime
    finalSearchTime = datetime.datetime.combine(today, searchTime)
    qexpy = finalSearchTime + datetime.timedelta(minutes=45)
    q = finalSearchTime
    print finalSearchTime
    print qexpy
    oldreqs = db((db.requests.rtime < q) & (db.requests.expiry > q) & (db.requests.place == request.vars.place)).select()
    #oldreqs = db((db.requests.rtime < q)  & (db.requests.place == request.vars.place)).select()
    print
    if(len(oldreqs) == 0):
        print 'no request, inserting in request and chat'
#        try:
#            rid = db.requests.insert(user_id=auth.user_id, place = request.vars.place, rtime = q, expiry = qexpy, foodtype=request.vars.foodtype)
#            db.chat.insert(rid=rid, user_id = auth.user_id)
#        except:
#            pass
        return "<div>No current request, We will notify you shortly</div>"
    else:
        print oldreqs
        print ' got output'
        #one = oldreqs[0]
        #print one
        s=""
        for one in oldreqs:
            cnt = len( db( (db.requests.id == one['id']) &  (db.chat.rid == db.requests.id) ).select(db.chat.user_id) )
            s += '<div style="border:3px solid green; width: 310px; margin: 12px; margin-left: 4%; height: 80px; float:left; border-radius: 8px; text-align:center; padding-top:2%" onclick="moredetails()"> <p> ' + str(cnt) + ' people going to ' + one['place']  + ' at ' +  str(one['rtime'])[11:16]  + '</p></div>'
        print s
        #s="<p> " +  oldreqs[0]['place']+" </o>"
        return s
        #return "<div>Output" + oldreqs[0]['id'] +"</div>"

def search():
    return locals()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
