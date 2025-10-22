# Examination 4 - Install a Web Server

Now that we know how to install software on a machine through Ansible, we can
begin to look at how to set up a machine with services.

A typical use case is how to get a web server up and running, and coincidentally
we happen to have one of our hosts named `webserver`.

As in the previous examination, we can use the [ansible.builtin.package](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/package_module.html)
module to install the prerequisite software.

Create a new file, you can call it what you like, but in the example below, it's referred to as
`webserver.yml`.

    ---
    - name: Install a webserver
      hosts: web
      become: true
      tasks:
        - name: Ensure nginx is installed
          ansible.builtin.package:
            name: nginx
            state: latest

        - name: Ensure nginx is started at boot
          ansible.builtin.service:
            name: nginx
            enabled: true

The above is a playbook that will install [nginx](https://nginx.org/), a piece of software that can
act as a HTTP server, reverse proxy, content cache, load balancer, and more.

Now, we can run `curl` to see if web server does what we want it to (serve HTTP pages on TCP port 80):

    $ curl -v http://<IP ADDRESS OF THE WEBSERVER>

Change the text within '<' and '>' to the actual IP address of the web server. It may work with the
name of the server too, but this depends on how `libvirt` and DNS is set up on your machine.

Is the response what we expected?

    $ curl -v http://192.168.121.10
    *   Trying 192.168.121.10:80...
    * connect to 192.168.121.10 port 80 from 192.168.121.1 port 46036 failed: Connection refused
    * Failed to connect to 192.168.121.10 port 80 after 0 ms: Could not connect to server
    * closing connection #0
    curl: (7) Failed to connect to 192.168.121.10 port 80 after 0 ms: Could not connect to server

# QUESTION A

Refer to the documentation for the [ansible.builtin.service](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/service_module.html)
module.

How can we make the web server start with an addition of just one line to the playbook above?

In the ansible.builtin.service task, you can add: 
```yml
state: started
```

# QUESTION B

You make have noted that the `become: true` statement has moved from a specific task to the beginning
of the playbook, and is on the same indentation level as `tasks:`.

What does this accomplish?

Placing become: true at the playbook level means all tasks in the playbook will run with elevated privileges (sudo).
You no longer need to specify become: true individually for each task.

# QUESTION C

Copy the above playbook to a new playbook. Call it `04-uninstall-webserver.yml`.

Change the ordering of the two tasks. Make the web server stop, and disable it from starting at boot, and
make sure that `nginx` is uninstalled. Change the `name:` parameter of each task accordingly.

Run the new playbook, then make sure that the web server is not running (you can use `curl` for this), and
log in to the machine and make sure that there are no `nginx` processes running.

Why did we change the order of the tasks in the `04-uninstall-webserver.yml` playbook?

First we stop and disable the service, then we uninstall the package.
If we uninstalled nginx first, the service might still be running, causing errors or leaving processes behind.
Ensures a clean and idempotent removal of the web server.


# BONUS QUESTION

Consider the output from the tasks above, and what we were actually doing on the machine.

What is a good naming convention for tasks? (What SHOULD we write in the `name:` field`?)


❯ curl -v http://192.168.121.148
*   Trying 192.168.121.148:80...
* connect to 192.168.121.148 port 80 from 192.168.121.1 port 36652 failed: Förbindelsen förvägrad
* Failed to connect to 192.168.121.148 port 80 after 0 ms: Couldn't connect to server
* Closing connection
curl: (7) Failed to connect to 192.168.121.148 port 80 after 0 ms: Couldn't connect to server

--------------------------------------------------------------------------------

❯ nano webserver.yml
❯ ansible-playbook webserver.yml

PLAY [Install a webserver] *************************************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************
ok: [192.168.121.148]

TASK [Ensure nginx is installed] *******************************************************************************************************
ok: [192.168.121.148]

TASK [Ensure nginx is started at boot] *************************************************************************************************
changed: [192.168.121.148]

PLAY RECAP *****************************************************************************************************************************
192.168.121.148            : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

❯ curl -v http://192.168.121.148
*   Trying 192.168.121.148:80...
* Connected to 192.168.121.148 (192.168.121.148) port 80
> GET / HTTP/1.1
> Host: 192.168.121.148
> User-Agent: curl/8.5.0
> Accept: */*
> 
< HTTP/1.1 200 OK
< Server: nginx/1.20.1
< Date: Wed, 22 Oct 2025 14:09:36 GMT
< Content-Type: text/html
< Content-Length: 5760
< Last-Modified: Mon, 24 Mar 2025 16:15:24 GMT
< Connection: keep-alive
< ETag: "67e1851c-1680"
< Accept-Ranges: bytes
< 
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
	<head>
		<title>Test Page for the HTTP Server on AlmaLinux</title>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<style type="text/css">
			/*<![CDATA[*/
			body {
				background-color: #fff;
				color: #000;
				font-size: 1.1em;
				font-family: "Red Hat Text", Helvetica, Tahoma, sans-serif;
				margin: 0;
				padding: 0;
                border-bottom: 30px solid #082336;
				min-height: 100vh;
				box-sizing: border-box;
			}
			:link {
				color: #304B5E;
			}
			:visited {
				color: #304B5E;
			}
			a:hover {
				color: #0069DA;
			}
			h1 {
				text-align: left;
				margin: 0;
				margin-bottom: .6em;
				padding: 1em 2em 1.5em 2em;
				background-color: #082336;
				color: #fff;
				font-weight: normal;
				font-size: 2.5em;
				border-bottom: 2px solid #000;
			}
            h1 img {
                border: none;
                margin-bottom: .4em;
            }
			h1 strong {
				font-weight: bold;
			}
			h2 {
				font-size: 1.1em;
				font-weight: bold;
			}
			hr {
				display: none;
			}
			.content {
				padding: 1em 5em;
			}
			.content-columns {
				/* Setting relative positioning allows for
				absolute positioning for sub-classes */
				position: relative;
				padding-top: 1em;
                display: flex;
				flex-wrap: wrap;
			}
			.content-column-left {
				/* Value for IE/Win; will be overwritten for other browsers */
				width: 47%;
				padding: 15px 30px;
				margin-right: 30px;
				padding-bottom: 2em;
				margin-bottom: 1em;
				flex: 1;
			}
			.content-column-left hr {
				display: none;
			}
			.content-column-right {
				/* Values for IE/Win; will be overwritten for other browsers */
				width: 47%;
				padding: 15px 30px;
				padding-bottom: 2em;
                margin-right: 30px;
				margin-bottom: 1em;
				flex: 1;
			}
			.content-columns>.content-column-left, .content-columns>.content-column-right {
				/* Non-IE/Win */
                border: 1px solid #d2d2d2;
				border-radius: 3px;
				box-sizing: border-box;
			}
			.logos {
				text-align: left;
				margin-top: 2em;
			}
            .logos a img {
                padding-right: 1.5em;
                margin-right: 1.5em;
                border-right: 1px solid #d2d2d2;
            }
			img {
				border: 2px solid #fff;
				padding: 2px;
				margin: 2px;
			}
			a:hover img {
				border: 2px solid #f50;
			}
			.footer {
			    font-size: xx-small;
                padding: 0 10em;
			    padding-bottom: 5em;
			}

            /* Responsive layout */
            @media (max-width: 800px) {
                .content-column-right, .content-column-left {
                flex: 100%;
                }
            }
			/*]]>*/
		</style>
	</head>

	<body>
		<h1>
            <img src="system_noindex_logo.png" alt="AlmaLinux Logo" /><br />
            Web Server <strong>Test Page</strong>
        </h1>

		<div class="content">
			<div class="content-middle">
				<p>This page is used to test the proper operation of the HTTP server after it has been installed. If you can read this page, it means that the HTTP server installed at this site is working properly.</p>
			</div>
			<hr />

			<div class="content-columns">
				<div class="content-column-left">
					<h2>If you are a member of the general public:</h2>

					<p>The fact that you are seeing this page indicates that the website you just visited is either experiencing problems, or is undergoing routine maintenance.</p>

					<p>If you would like to let the administrators of this website know that you've seen this page instead of the page you expected, you should send them e-mail. In general, mail sent to the name "webmaster" and directed to the website's domain should reach the appropriate person.</p>

					<p>For example, if you experienced problems while visiting www.example.com, you should send e-mail to "webmaster@example.com".</p>

					<p>For information on AlmaLinux, please visit the <a href="https://almalinux.org">AlmaLinux website</a>. The documentation for AlmaLinux is <a href="https://wiki.almalinux.org">available in AlmaLinux wiki</a>.</p>
					<hr />
				</div>

				<div class="content-column-right">
					<h2>If you are the website administrator:</h2>

					<p>You may now add content to the webroot directory. Note
					that until you do so, people visiting your website will see
					this page, and not your content.</p>

					<p>For systems using the Apache HTTP Server:
					You may now add content to the directory <tt>/var/www/html/</tt>. Note that until you do so, people visiting your website will see this page, and not your content. To prevent this page from ever being used, follow the instructions in the file <tt>/etc/httpd/conf.d/welcome.conf</tt>.</p>

					<p>For systems using NGINX:
					You should now put your content in a location of your
					choice and edit the <code>root</code> configuration directive
					in the <strong>nginx</strong> configuration file
					<code>/etc/nginx/nginx.conf</code>.</p>

					<div class="logos">
						<a href="https://almalinux.org"><img src= "/icons/poweredby.png" alt="[ Powered by AlmaLinux ]" /></a>
						<img src= "poweredby.png" alt="[ Powered by AlmaLinux ]" />
					</div>
				</div>
			</div>
		</div>
	<div class="footer">
		<a href="https://apache.org">Apache&trade;</a> is a registered trademark of <a href="https://apache.org">the Apache Software Foundation</a> in the United States and/or other countries.
        <br />
		<a href="https://nginx.com">NGINX&trade;</a> is a registered trademark of <a href="https://www.f5.com">F5 Networks, Inc.</a>.
	</div>
	</body>
</html>
* Connection #0 to host 192.168.121.148 left intact

-----------------------------------------------------------------------------------------

 nano 04-uninstall-webserver.yml
❯ ansible-playbook 04-uninstall-webserver.yml
[WARNING]: Could not match supplied host pattern, ignoring: web

PLAY [Uninstall webserver] *************************************************************************************************************
skipping: no hosts matched

PLAY RECAP *****************************************************************************************************************************

❯ nano 04-uninstall-webserver.yml
❯ ansible-playbook 04-uninstall-webserver.yml

PLAY [Uninstall webserver] *************************************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************
ok: [192.168.121.148]

TASK [Stop and disable nginx service] **************************************************************************************************
changed: [192.168.121.148]

TASK [Uninstall nginx] *****************************************************************************************************************
changed: [192.168.121.148]

PLAY RECAP *****************************************************************************************************************************
192.168.121.148            : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

❯ curl -v http://192.168.121.148
*   Trying 192.168.121.148:80...
* connect to 192.168.121.148 port 80 from 192.168.121.1 port 49808 failed: Förbindelsen förvägrad
* Failed to connect to 192.168.121.148 port 80 after 0 ms: Couldn't connect to server
* Closing connection
curl: (7) Failed to connect to 192.168.121.148 port 80 after 0 ms: Couldn't connect to server

----------------------------------------------------------------------------------------

❯ curl -v http://192.168.121.148
*   Trying 192.168.121.148:80...
* connect to 192.168.121.148 port 80 from 192.168.121.1 port 49808 failed: Förbindelsen förvägrad
* Failed to connect to 192.168.121.148 port 80 after 0 ms: Couldn't connect to server
* Closing connection
curl: (7) Failed to connect to 192.168.121.148 port 80 after 0 ms: Couldn't connect to server
❯ ssh -i /home/gato/devops24/devops24/lab_environment/deploy_key deploy@192.168.121.148

Last login: Wed Oct 22 14:19:45 2025 from 192.168.121.1
[deploy@webserver ~]$ ps aux | grep nginx
deploy     13439  0.0  0.4   6384  2176 pts/0    S+   14:24   0:00 grep --color=auto nginx
