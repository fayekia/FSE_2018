import os
import MySQLdb

emails = {}

uids = set()

bugs_assignee = {}

bugs_assignee_changes = {}

# alias = {} 

rs = ()

try:
    conn = MySQLdb.connect(host="localhost",user="***",passwd="***",db="eclipse2011",port=3306)
    cur = conn.cursor()
    cur.execute("select bugs.bug_id, bugs.assigned_to from bugs;")
    rs = cur.fetchall()
    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print "Mysql Error"
    sys.exit()

for n in rs:
    bugs_assignee[n[0]] = n[1]
    uids.add(n[1])

rs = ()

try:
    conn = MySQLdb.connect(host="localhost",user="***",passwd="***",db="eclipse2011",port=3306)
    cur = conn.cursor()
    cur.execute("select bug_id,UNIX_TIMESTAMP(bug_when),fieldid,removed,added from bugs_activity;")
    rs = cur.fetchall()
    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print "Mysql Error"
    sys.exit()

for n in rs:
    if n[2] != 15:
        continue
    if not bugs_assignee_changes.has_key(n[0]):
        bugs_assignee_changes[n[0]] = []
    bugs_assignee_changes[n[0]].append([n[1],n[3],n[4]])

e_cnt = 0

for k,v in bugs_assignee_changes.iteritems():
    flag = True
    newl  = sorted(v,key=lambda x:x[0])
    l = len(newl)
    for i in range(0,l-1):
        if newl[i][2] != newl[i+1][1]:
            flag = False
#            print(str(newl[i])+str(newl[i+1]))
            break
    if flag == False:
    	e_cnt += 1
#        continue
    emails[newl[0][1]] = -1
    bugs_assignee_changes[k] = newl

print(e_cnt)

for k,v in bugs_assignee_changes.iteritems():
    emails[v[-1][2]] = bugs_assignee[k] 

'''
cnt = 0
for k,v in emails.iteritems():
	if v == -1:
		cnt += 1
print(len(emails))
print(cnt)
'''

maxuid = max(uids)
print(maxuid)
newid = maxuid + 10
for k,v in emails.iteritems():
    if v == -1:
        emails[k] = newid
        newid += 1

f_out = open("email_uid_map.txt","w")

for k,v in emails.iteritems():
    f_out.write(str(k)+";"+str(v)+"\n")

f_out.close()

f_out = open("bugs_assignee_init_final.txt","w")

for k,v in bugs_assignee.iteritems():
    f_out.write(str(k)+";"+str(v)+";")
    if bugs_assignee_changes.has_key(k):
        uid = emails[bugs_assignee_changes[k][0][1]]
        f_out.write(str(uid)+"\n")
    else:
        f_out.write(str(v)+"\n")

f_out.close()
