# sabermetrics
Scraping, munging and analysis of NHL data.

###Raw Format vs Condensed Format
To print condensed format you would set `condensed = True` in the
`ScrapePlayByPlay` function from the *nhl_soup.py* file.
```python
nhl_soup.ScrapePlayByPlay(url,workingDirectory,condensed=True)
```

###Required data-scraping Python packages
BeautifulSoup, html5lib, and Pandas.
