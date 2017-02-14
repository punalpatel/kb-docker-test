---
title: Hello from the BBQ
template: break-fix
id: 213730187
locale: en-us
author: timani
---


**Friday**

| ----- |
| Product |  Version |  
| **Pivotal Cloud Foundry® (PCF) Elastic Runtime&nbsp;** | 

&nbsp;1.7.x

 | 

**Symptom**

[AWS NAT gateways][1]&nbsp;**were introduced in the Elastic Runtime 1.7 cloud formation scripts for&nbsp;deploying to Amazon Web Services (AWS). One possible error you may see that indicates that you are having issues with the AWS Network Address Translation (NAT) gateway is if you find that the Apps Manager errand does not complete. You may also see that it times out before it can complete as shown below**:
    
    
    Started running errand &gt; push-apps-manager/0. Failed: Timed 
    out sending `run_errand' 
    to 31d2a6d4-d136-4b12-a53c-3c33fe3101ee after 45 seconds (00:00:45)
    
    Error 450002: Timed out sending `run_errand' 
    to 31d2a6d4-d136-4b12-a53c-3c33fe3101ee after 45 seconds

**Cause**

**The AWS NAT gateway can sometimes have delays or timeouts for some hairpin NAT traffic back to the Elastic Runtime load balancer when using Transport Layer Security (TLS) protocol**.

**Resolution**

**To work around this issue, it is recommended to move from NAT gateways back to NAT EC2 instances that were previously used in versions prior to PCF ER 1.7**.  
**The&nbsp;following steps can be used to convert from using&nbsp;NAT gateway to using NAT instance**:

1. Log on to the AWS console.
2. **Create a NAT instance in the public subnet of your PCF VPC, and assign it a public IP. You can find the AMI ID of the supported Amazon NAT instances by searching the public AMI list for "amzn-ami-vpc-nat" and picking one of those. We usually use 64-bit HVM instances, of size t2.medium (or larger if you need more bandwidth).**&nbsp;[[1][2]]
3. **Disable source-destination checking on your newly booted NAT instance.**
4. **Within your VPC, change all the route tables**&nbsp;[[2][3]]&nbsp;**(there might be just one) that currently uses your NAT gateway as the default route (0.0.0.0/0) to use your NAT instance instead.**
5. **You can create 1 NAT instance for each availability zone (AZ), or you can dump all the traffic into a single NAT instance. That depends on how much production availability you require, and how much traffic you expect. All NAT instances must be booted in a public subnet (a subnet with the IGW as the default route), and have src/dest checking disabled, so you'll need many public subnets if you want to have truly reliable multi-AZ setup.**
6. **You can leave the NAT gateway in place, it won't be used as you have changed your route tables to use the NAT instance(s) that you have created. You can, if you wish, delete the NAT Gateway to reduce&nbsp;cost**.

Some more information can be found [here][4],&nbsp;[3]&nbsp;for NAT instances with Pivotal Cloud Foundry.

**Continued investigations by R&amp;D**

**R&amp;D&nbsp;will deliver a new cloud formation template in due course and are&nbsp;also investigating the issue with AWS in the hopes of fixing the issue so that we can use&nbsp;NAT gateways in the future**.

**Additional Information**

For further information, please refer to the following resources:&nbsp;

[1]: http://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/vpc-nat-gateway.html
[2]: https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_NAT_Instance.html#NATInstance
[3]: https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_NAT_Instance.html#nat-routing-table
[4]: http://docs.pivotal.io/pivotalcf/1-7/customizing/pcf-aws-manual-config.html#pcfaws-nat

  </http:></https:></https:>
