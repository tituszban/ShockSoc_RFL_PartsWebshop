# ShockSoc_RFL_PartsWebshop

This is a flask web server, hosted on AWS: http://ec2-35-176-114-206.eu-west-2.compute.amazonaws.com/
The porpuse of this app to generate a reciept for people wanting to purchuse parts for Robot Figthing League. There is no monetary transaction on this site.
This is the first web app I've ever done. Given that, I'm pretty happy with it!

It takes a user, assignes him with a session id, requests for identification information (SSID, email, name), than serves an automatically populated html page with all the available parts, using jinja2. A number can be entered to order an item. It takes the user to a review page to confirm the order, and than loads a page, that prints automatically the reciept.

Used: python 3.6, flask, html, jinja2
