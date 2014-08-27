# WiTables

## The missing view on your PyTables.

> WiTables is a web-based visualization tool for PyTables written in python. Deploy on it your server and access immediately to your data.
> As a web application, databases can be shared with people and accessed from everywhere.

### Version Name: Stig

A lot of work to do but the basics are here.

To Do Now:

* jQuery order tables
* rewrite mod to access the data directly from the navigation bar
* Manage sessions to keep history
* Search bar

___

### Security

**Important!** Depending on your web server configuration, WiTables can be public on the internet. Be really careful, your data may go online and worst, the could be modify by anybody.
By default, WiTables comes with .htaccess file that restrains access to localhost, local network and VPN (127.0.0.1, 192.168.0.X, 10.8.0.X).

**You are responsible!** The current version is in read-only mode, but we are not responsible for the lost for your data.
> backup your data regularly!
- Albert Einstein


### Getting Started

#### Dependencies

* Python 2.x
* PyTables 3.x
* WebServer (that enables python applications)

#### Install a web server and it's (almost) done

* Install Pytables
* Install your favorite web server that enables python script on your machine.
* Download the source and copy them in your web directory.
* Enable python script on your web server.
* Create a link to your database folder.
* That'it!

#### Example with Apache on Linux

##### Install PyTables

[PyTables installation guide](http://pytables.github.io/usersguide/installation.html)

##### Install mod_wsgi module

[mod_wsgi on code.google.com](https://code.google.com/p/modwsgi/wiki/InstallationInstructions)

On Apache 2, you may need to modify your 000-default.conf website by adding:
```xml
	 <Directory "/var/www/witables/">
 		AllowOverride All
	 </Directory>
```
At this point, you should be able to see the main page at this address:
[http://localhost/witables](http://localhost/witables)

##### Create a link to your databases.

Now, go to the witables source folder and type:

```bash
ln -s path_to_my/pytables/database database
```

You're done.

___

#### Next Version: Wiche Lorraine

### Have fun with your data, you sexy geek.
