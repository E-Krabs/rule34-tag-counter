# rule34_json_dump
<h3><b>About</b></h3>
Create a SQLite database of rule34, and analyze what content is most popular.<br>

Every image on rule34 must be tagged with info describing what's in it cause its a <a href="https://booru.org/">Borru</a>. Using this information provided via the <a href="https://api.rule34.xxx/">rule34 API</a>, we can plot the popularity of something on rule34 and save eveything to a local database.

<h3><b>Fetching Data</b></h3>
This project fetches data from rule34 provided via the <a href="https://api.rule34.xxx/">rule34 API</a>. <code>fetchall.py</code> collects as much data as it can. This opperation can take a few hours (~5hr), because too many requests too fast, the server will restrict our ip. Every request returns 1000 posts. The script writes the returned results to a SQLite database for later analysis.

<hr>
<ul>
  <li><code>fetchall.py</code> Dumps https://api.rule34.xxx. Dumps as much as it can (~5,118,998). Takes ~5 hours to complete.<br>
</ul>

<h3><b>How To Use?</b></h3>
<ul>
  <li>Cd to the repo: <code>cd C:/Users/User/Downloads/rule34-tag-counter-main</code></li>
  <li>Install requirements: <code>pip install -r requirements.txt</code></li>
  <li>Generate data-set: <code>python3 fetchall.py</code> (This will take many hours. Tqdm will let you know with a progress bar.)</li>
  <li>#in progress# Generate <code>report</code>: <code>python3 sqlite_count.py</code> (Should only take ~3min)</li>
  <li>profit?</li>
</ul>

<h3><b>Requirements:</b></h3>
<ul>
  import os, 
import sqlite3, 
import json, 
import pandas as pd, 
import matplotlib.pyplot as plt, 
import matplotlib.dates, 
from tqdm import tqdm, 
</ul>
