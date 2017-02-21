---
title: Test KB
template: how-to
id: 
locale: en-us
---

# Test KB

**Environment**
Product

**Symptom**

If you see issues where VM's are using unusually high amounts of memory, you may be affected by the following bug where Rsyslogd uses excessive amounts of memory.

**Cause**

There is a memory leak in Rsyslogd 8.23.0 which is the version used in PCF1.8.21-build.1 in Stemcell 3263.12.  


**Resolution**

You will need to upgrade your Stemcell to version 3263.15 or later. In this version, the Ubuntu stemcells have been PIN'ed to _rsyslog_ to 8.22.0.

