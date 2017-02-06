from jobspy.modules.jobbean import *

def sim_dup(hash1,hash2):
    hashsame = 0
    for i in range(min(len(hash1),len(hash2))):
        if hash1[i] == hash2[i]:
            hashsame += 1
    if hashsame > min(len(hash1),len(hash2)) - 2:
        return True
    else:
        return False

def __dup(suspects,hash,url):
    for suspect in suspects:
        suspect_hash = suspect.hash
        if sim_dup(suspect_hash,hash):
            with open('dup.txt','a') as fhdl:
                fhdl.write("%s\t%s\t%s\t%s\n" % (url,suspect_hash,hash,suspect.url))
            return True        
    return False

def has_dup(hash,time,url):
    hash1 = hash[:16]
    hash2 = hash[16:32]
    hash3 = hash[32:48]
    hash4 = hash[48:]
    date = time.split(' ')[0]

    suspects = SimDup1.where(hashpart=hash1,date=date).select()
    if __dup(suspects,hash,url):
        return True
       
    suspects = SimDup2.where(hashpart=hash2,date=date).select()
    if __dup(suspects,hash,url):
        return True

    suspects = SimDup3.where(hashpart=hash3,date=date).select()
    if __dup(suspects,hash,url):
        return True

    suspects = SimDup4.where(hashpart=hash4,date=date).select()
    if __dup(suspects,hash,url):
        return True

    return False

def insert_dup(hash,url,time):
    hash1 = hash[:16]
    hash2 = hash[16:32]
    hash3 = hash[32:48]
    hash4 = hash[48:]
    date = time.split(' ')[0]
    
    sim1 = SimDup1()
    sim1.hashpart = hash1
    sim1.hash = hash
    sim1.url = url
    sim1.time = time
    sim1.date = date

    sim2 = SimDup2()
    sim2.hashpart = hash2
    sim2.hash = hash
    sim2.url = url
    sim2.time = time
    sim2.date = date

    sim3 = SimDup3()
    sim3.hashpart = hash3
    sim3.hash = hash
    sim3.url = url
    sim3.time = time
    sim3.date = date

    sim4 = SimDup4()
    sim4.hashpart = hash4
    sim4.hash = hash
    sim4.url = url
    sim4.time = time
    sim4.date = date


    sim1.save()
    sim2.save()
    sim3.save()
    sim4.save()
