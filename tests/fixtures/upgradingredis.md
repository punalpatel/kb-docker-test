template: break-fix
id:
locale: en-us
# Upgrading Redis from 1.6.0 - 1.6.3 to 1.7.x Fails – All Help & Support

**Environment**

| ----- |
|  Product |   Version |  
|  Pivotal Cloud Foundry® (PCF) Redis |   1.6 / 1.7 | 

**Symptom**

Upgrading Redis from 1.6.x (where x < 4) to 1.7.x fails and results in the following error: 
    
    
    Started updating job cf-redis-broker > cf-redis-broker/0 (0ca57e86-a242-4424-bc25-b2203c7b7249) (canary). Failed: Action Failed get_task: Task 89a6e064-e8bd-481e-7339-cfa5bb76c16c result: Applying: Reloading jobSupervisor: Failed to reload monit: before=1483531146 after=1483531146 (00:01:55)
    
    Error 450001: Action Failed get_task: Task 89a6e064-e8bd-481e-7339-cfa5bb76c16c result: Applying: Reloading jobSupervisor: Failed to reload monit: before=1483531146 after=1483531146
    
    Task 1236 error
    
    For a more detailed error report, run: bosh task 1236 --debug  
    ===== 2017-01-04 12:30:26 UTC Finished "bundle exec bosh -n deploy"; Duration: 119s; Exit Status: 1  
    Exited with 1.** **

**Cause**

Redis' process-destroyer job fails to gracefully shutdown because of an unhandled exit-code on the CF-Redis-Broker VM. 

**Resolution**  
Re-attempt an upgrade with no changes (click "Apply changes"). The second attempt should succeed. This issue is fixed in 1.6.4.
