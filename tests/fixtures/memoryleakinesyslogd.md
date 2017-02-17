---
title: Post with ID!
template: break-fix
id: 3213131213
locale: en-us
---
# Memory Leak in Rsyslogd

**Environment**

| ----- |
| 

 Product

 | 

 Version

 |  
| 

 Pivotal Cloud Foundry®  (PCF) Elastic Runtime 

 | 

 1.8.21-build.1

 (bosh-stemcell-3263.12)

 | 

**Symptom**

If you see issues where VM's are using unusually high amounts of memory, you may be affected by the following bug where Rsyslogd uses excessive amounts of memory.

**Cause**

There is a memory leak in Rsyslogd 8.23.0 which is the version used in PCF1.8.21-build.1 in Stemcell 3263.12.  

For example, check for errors like the following in your message logs (/var/log/messages):
    
    
    Jan 3 16:39:24 localhost vmsvc[838]: [ warning] [guestinfo] Failed to get vmstats. 
    Jan 3 16:39:24 localhost rsyslogd: action 'action 0' resumed (module 'builtin:omfwd') [v8.23.0 try http://www.rsyslog.com/e/2359 ]
    
     

You can check the version of _rsyslogd_ that you are using by SSH'ing onto a VM and running the following command: **rsyslogd -version** 

**Resolution**

You will need to upgrade your Stemcell to version 3263.15 or later. In this version, the Ubuntu stemcells have been PIN'ed to _rsyslog_ to 8.22.0.

**Additional Information**

To check the amount of memory being consumed by _rsyslogd_, please run the following command:

**`ps auxw | grep rsyslogd | grep -v grep`**

For more information on this bug, please click [here][1] 1.

1.    

[1]: https://github.com/cloudfoundry/bosh/issues/1537%20
