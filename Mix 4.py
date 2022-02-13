from ldap3 import Server, Connection, SAFE_SYNC


f = '''
config user group\n
'''
e = '''
end
'''

server = Server('<LDAP IP>')
conn = Connection(server, '<Username>', '<Password>', client_strategy=SAFE_SYNC, auto_bind=True)

pns = open("PNS.txt")
yt = open("YT.txt")
# ceo = open("CEO.txt")
admins = open("Admins.txt")
mail = open("Mail.txt")
social_network = open("Social Network.txt")

# lists = [pns, yt, ceo, admins, mail]
lists = [social_network, yt, pns, admins, mail]
users_pns = set()
users_yt = set()
users_admins = set()
users_mail = set()
users_social_network = set()

new_groups = []
for i in range(len(lists)):
    for j in range(i+1, len(lists)):
        for k in range(j+1, len(lists)):
            for l in range(k+1, len(lists)):
                new_groups.append(open("{0}&{1}&{2}&{3}.txt".format(lists[i].name[:-4],lists[j].name[:-4], lists[k].name[:-4], lists[l].name[:-4]), 'a'))
        

users = [users_social_network, users_yt, users_pns, users_admins, users_mail]
for i in range(len(lists)):
    for u in lists[i]:
        users[i].add(u.split()[1])
print(len(new_groups))
idx = 0
for i in range(len(lists)):
    for j in range(i+1, len(lists)):
        for k in range(j+1, len(lists)):
            for l in range(k+1, len(lists)):
                common = users[i] & users[j] & users[k] & users[l]
                new_groups[idx].seek(0)
                new_groups[idx].write(f)
                print(idx)
                print(new_groups[idx].name)
                for u in common:
                    status, result, response, _ = conn.search('dc=enppi,dc=com', '(employeeID={0})'.format(u))
                    if len(response) == 4:
                        x=    '''
                    edit "{0}&{1}&{2}&{3}_UsersGR"
                    set group-type fsso-service
                    append member \"{4}\"
                    next\n
                        '''.format(lists[i].name[:-4],lists[j].name[:-4],lists[k].name[:-4],lists[l].name[:-4],response[0]['dn'])
                        new_groups[idx].write(x)
                new_groups[idx].write(e)
                idx += 1
for k in new_groups:
    k.close()

    
        