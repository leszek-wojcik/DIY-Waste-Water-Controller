html_head = b"""
<!DOCTYPE html>
<html>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/3/w3.css">
<head> <title>DIY Wastewater Controller</title> </head>
<body class="w3-light-grey">
<div class="w3-content w3-margin-top" style="max-width:1200px;">
<div class="w3-row-padding">
"""

html_left_column_head = b"""
<div class="w3-quarter w3-margin-bottom">
<div class="w3-white w3-text-grey w3-card-4">
<div class="w3-container">
<h1>DIY Wastewater Controller</h1>
</div>
<div class="w3-container">
<hr>
<p class="w3-large"><b>Controller Status</b></p>
<hr>
"""

html_left_column_manual_control = b"""
Control
<div class="w3-display-container">
<div class="w3-panel w3-teal w3-round"> %s </div>
</div>
"""

html_left_column_areation = b"""
Areation 
<div class="w3-display-container"> 
<div class="w3-panel w3-teal w3-round"> %s </div>
</div>
"""

html_left_column_circulation = b"""
Circulation 
<div class="w3-display-container"> 
<div class="w3-panel w3-teal w3-round"> %s </div>
</div>
"""

html_left_column_controller_time = b"""
Controller Time
<div class="w3-display-container"> 
<div class="w3-panel w3-teal w3-round"> %s </div>
</div>
"""

html_left_column_controller_temperature = b"""
Controller Temperature
<div class="w3-display-container"> 
<div class="w3-panel w3-teal w3-round"> %s </div>
</div>
"""

html_left_column_controller_humidity = b"""
Controller Humidity
<div class="w3-display-container"> 
<div class="w3-panel w3-teal w3-round"> %s </div>
</div>
"""

html_left_column_service_reminder = b"""
Service Remider
<div class="w3-display-container"> 
<div class="w3-panel w3-teal w3-round"> %s </div>
</div>
"""

html_left_column_end = b"""
<hr>
</div>
</div>
</div>
"""

html_right_column_head = b"""
<div class="w3-threequarter w3-animate-top">
<div class="w3-container w3-card w3-white w3-margin-bottom">
"""

html_right_column_time = b"""
<h2 class="w3-text-grey">Controller Settings</h2>
<hr>
<h4 class="w3-text-grey w3-padding-16">Set time and date</h4>
<div class="w3-container">
<form>
<input class="w3-half w3-input" type="date" name="date" value="2018-09-01">
<input class="w3-half w3-btn w3-teal w3-round-xlarge" type="submit" value="Set Date">
</form>
</div>
<div class="w3-container">
<form>
<input class="w3-half w3-input" type="time" name="time" value="20:00">
<input class="w3-half w3-btn w3-teal w3-round-xlarge" type="submit" value="Set Time">
</form>
</div>
"""

html_right_column_reminder = b"""
<h4 class="w3-text-grey w3-padding-16">Set service reminder date</h4>
<div class="w3-container">
<form>
<input class="w3-half w3-input" type="date" name="reminder" value="2018-09-01">
<input class="w3-half w3-btn w3-teal w3-round-xlarge"  type="submit" value="Set Date">
</form>
</div>
<br>
</div>
"""

html_right_column_control_head = b"""
<div class="w3-container w3-card w3-white w3-margin-bottom">
<h2 class="w3-text-grey">Manual Control</h2>
<hr>
<h4 class="w3-text-grey w3-padding-16"> Select control mode </h4>
"""

html_right_column_control_form = b"""
<form class="w3-container">
<div class="w3-half w3-container">
<input class="w3-radio" type="radio" name="control_method" value="auto"> <label>Auto</label>
<input class="w3-radio" type="radio" name="control_method" value="manual"> <label>Manual</label>
<input class="w3-radio" type="radio" name="control_method" value="holiday"> <label>Holiday</label>
</div>
<input class="w3-half w3-btn w3-teal w3-round-xlarge w3-block" type="submit" value="Set">
</form>
<br>
<div class="w3-text-gray">When manual operation mode is enabled user is able to control areation and circulation manualy.</div>
<br>
<form class="w3-container">
<input class="w3-btn w3-teal w3-round-xlarge w3-block" type="submit" name="control" value="areation">
<br>
<input class="w3-btn w3-teal w3-round-xlarge w3-block" type="submit" name="control" value="circulation">
</form>
<br>
</div>
"""

html_right_column_about = b"""
<div class="w3-container w3-card w3-white w3-margin-bottom">
<h2 class="w3-text-grey">About</h2>
<hr>
<div class="w3-text-grey w3-padding-16">
<p>DIY Waste Water Controller project is copy protected under MIT licence</p>
<p>Copyright (c) 2018 Leszek Wojcik</p>
<p>Follow project on GitHub or Hackaday</p>
<a class="w3-bar-item w3-btn w3-small" href="https://hackaday.io/project/160407" target="_blank">Hackaday</a>
<a class="w3-bar-item w3-btn w3-small" href="https://github.com/leszek-wojcik/DIY-Waste-Water-Controller" target="_blank">GitHub</a>
</div>
</div>
</div>
"""

html_footer = b"""
</div>
</div>
</html>
"""
