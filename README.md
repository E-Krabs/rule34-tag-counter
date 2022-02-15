# rule34_json_dump
<h3><b>About</b></h3>
Scripts to analyze create database of rule34, and analyze what content is most popular.<br>

Every image on rule34 must be tagged with info describing what's in it cause its a <a href="https://booru.org/">Borru</a>. Using this information provided via the <a href="https://api.rule34.xxx/">rule34 API</a>, we can plot the popularity of something on rule34 and save eveything to a local database.

<h3><b>Fetching Data</b></h3>
This project fetches data from rule34 provided via the <a href="https://api.rule34.xxx/">rule34 API</a>. <code>fetchall.py</code> collects as much data as it can. This opperation can take a few hours (~5hr), because too many requests too fast, the server will restrict our ip. Every request returns 1000 posts. The script writes the returned results to a SQLite database for later analysis.

<hr>
<ul>
  <li><code>updated_fetchall.py</code> Dumps https://api.rule34.xxx. Dumps as much as it can (~5,118,998). Takes ~5 hours to complete.<br>

<h3><b>Requirements:</b></h3>
<ul>
  <li>matplotlib==3.5.1</li>
  <li>pandas==1.3.5</li>
  <li>seaborn==0.11.2</li>
  <li>requests==2.26.0</li>
  <li>tqdm==4.62.3</li>
  <li>xmltodict==0.12.0</li>
</ul>
