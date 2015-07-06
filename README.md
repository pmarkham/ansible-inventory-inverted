# Ansible Inverted Inventory

## Warning

This is proof of concept code only and has not been used in a real environment. __Use it at you own risk.__

We haven't decided if this is a good idea yet, so this may never be developed further.

## What?

The inventory in Ansible is arranged in a hierarchical layout. It's not a single hierarchy, like a directory structure on disk;
rather, you can have multiple hierarchies to suit your needs. The static inventory lets you specify this in a top-down manner by
defining groups and their children using the `[groupname:children]` syntax.

This script lets you specify groups in a bottom-up way by defining groups and their _parents_. The syntax for this is `[groupname:parents]`.

I haven't figured out a better name for it so it's currently know as the inverted inventory.

## Why?

We use Ansible's static inventory to specify the hosts and groups. We tend to use a lot of groups, which means we
end up specifying a host group in multiple parent groups.

For example, if we have a `sydney-webservers` groups, we could end up with the following:

```
[sydney-webservers]
sydweb01
sydweb02

[sydney:children]
sydney-webservers

[webserver:children]
sydney-webservers

[rhel6:children]
sydney-webservers

[abc-application]
sydney-webservers
```
If we wanted to add a `melbourne-webservers` group that was largely the same as the `sydney-webservers` group, we need to find all the parent groups and add it to each of them.

We decided to try something different. Using (abusing?) Ansible's dynamic inventory, we wrote a script that would read an .ini formatted inventory which lets you specify the parent groups:

```
[sydney-webservers]
sydweb01
sydweb02

[sydney-webservers:parents]
sydney
webserver
rhel6
abc-application
```
Now, if we wanted to add the `melbourne-webservers` group, we can just copy this and change the host list and `:parents` list.

```
[melbourne-webservers]
melweb01
melweb02

[melbourne-webservers:parents]
melbourne
webserver
rhel6
abc-application
```

You can also specify group variable using `[groupname:vars]`, the same as with the static inventory

A more complex example is:

```
[sydney-webservers]
sydweb01
sydweb02

[sydney-webservers:parents]
sydney
webservers

[sydney-webservers:vars]
subnet=10.1.1.0
netmask=255.255.255.0
router=10.1.1.1
    
[melbourne-webservers]
melweb01
melweb02

[melbourne-webservers:parents]
melbourne
webservers

[melbourne-webservers:vars]
subnet=10.1.2.0
netmask=255.255.255.0
router=10.1.2.1
    
[sydney-appservers]
sydapp01
sydapp02

[sydney-appservers:parents]
sydney
rhel6
    
[melbourne-appservers]
melapp01
melapp02

[melbourne-appservers:parents]
melbourne
rhel5
    
[sydney-database-servers]
syddb01
syddb02

[sydney-database-servers:parents]
oracle-rac
sydney
solaris-10-sparc
    
[melbourne-database-servers]
meldb01
meldb02

[melbourne-database-servers:parents]
oracle-rac
melbourne
solaris-10-sparc
    
[webservers:parents]
solaris-10-x86
    
[rhel5:parents]
rhel-common
  
[rhel5:vars]
repo=repo:/rhel5
    
[rhel6:parents]
rhel-common

[rhel6:vars]
repo=repo:/rhel6
    
[solaris-10-x86:parents]
solaris-10-common

[solaris-10-sparc:parents]
solaris-10-common

[sydney:vars]
dns-server=10.1.10.1

[melbourne:vars]
dns-server=10.1.11.1
```

## How?

You can use this script by dropping it in your inventory directory and making it executable. You can also specify it explicitly as the inventory, either on the command line, the ansible.cfg file or using environment variables.

## Future? ##

I've got no idea if we'll end up using this script. If nothing else, it's was a good exercise in learning how a dynamic inventory.