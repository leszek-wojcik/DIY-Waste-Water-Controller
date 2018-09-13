html = """<!DOCTYPE html>
<html>
<head> <title>DYI Waste Water Controller</title> </head>
<h2>Current state</h2>
<h4>Manual Control - %s</h4>
<h4>Areation - %s </h4>
<h4>Circulation - %s </h4>
<h4>Clock -  %s </h4>
<h4>Temperature - %s </h4>
<h4>Humidity - %s </h4>
<h2>Service reminder</h2></center>
<h4>Service: %s </h4>
<h2>Set Time and Date</h2>

<form>
Date:   <input type="date" name="date" value="2018-09-01">
<input type="submit" value="Set Date">
</form>

<form>
Time:   <input type="time" name="time" value="20:00">
<input type="submit" value="Set Time">
</form>

<h2>Manual Control</h2>
<form>
    <legend>Choose control</legend>
    <div>
        <input type="radio" id="control_method_auto" name="control_method" value="auto">
        <label for="control_method_auto">Auto</label>
        <input type="radio" id="control_method_manual" name="control_method" value="manual">
        <label for="control_method_manual">Manual</label>
    <input type="submit" value="Set">
    </div>
</form>

<form>
    <div>
        <input type="submit" name="control" value="areation">
    </div>
    <div>
        <input type="submit" name="control" value="circulation">
    </div>
</form>

<h2>Service Reminder</h2>
<form>
Date:   <input type="date" name="reminder" value="2018-09-01">
<input type="submit" value="Set Date">
</form>

</html>
"""
