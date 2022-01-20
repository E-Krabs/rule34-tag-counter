# rule34_json_dump
<h3><b>About</b></h3>
Scripts to analyze create database of rule34, and analyze what content is most popular.<br>

Every image on rule34 must be tagged with info describing what's in it (characters, artist, acts, etc.). Using this information provided via the <a href="https://api.rule34.xxx/">rule34 API</a>, we can plot the popularity of something on rule34.

<h3><b>Fetching Data</b></h3>
This project fetches data from rule34 provided via the <a href="https://api.rule34.xxx/">rule34 API</a>. <code>fetchall.py</code> collects as much data as it can. This opperation can take a few hours, because too many requests too fast, the server will ban us for abuse. Every request returns 1000 posts. The script writes the returned results to a JSON file (~?GB) for later analysis.

<hr>
<ul>
  <li><code>updated_fetchall.py</code> Dumps https://api.rule34.xxx. Dumps as much as it can (~?mil posts). Takes ~?-? hours to complete.<br>

<h3><b>Requirements:</b></h3>
<ul>
  <li>matplotlib</li>
  <li>pandas</li>
  <li>requests</li>
  <li>bigjson (if Memory < 64GB)</li>
</ul>