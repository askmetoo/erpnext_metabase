## Metabase for ERP

To Visualize Data 

#### License

MIT

## Table of Content:

* Installation Guide

### Install Pre-requisites

- Python => 2.7
- MySQL
- Frappe
- Java[Oracle/Open JDK]
	- [Install Oracle Java]("https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-get-on-ubuntu-16-04")
	- [Install Open JDL]("http://openjdk.java.net/install/")

### Install Metabase

* Step 1
	* Install Metabase using  bench get-app metabase https://github.com/navdeepghai1/metabase



* Step 2
	
	*  Add these enteries in supervisor.conf, if it's production mode

```
[program:frappe-bench-frappe-metabase]
command=/bin/bash  /home/<username>/frappe-bench/config/metabase
priority=3 
autostart=true
autorestart=true
stdout_logfile=/home/<username>/frappe-bench/logs/metabase.log
stderr_logfile=/home/<username>/frappe-bench/logs/metabase.error.log
user=<username>
directory=/home/<username>/frappe-bench	
```
	
	* For Development mode you can add


```
metabase: /bin/bash apps/metabase/metabase/library/execute
```

* Step 3:
	* Restart the supervisor service
	 
