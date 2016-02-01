# sabermetrics
Scraping, munging and analysis of NHL data.

###Raw Format vs Condensed Format
To change between the raw and condensed format you would comment and uncomment
the following lines in *nhl_soup.py*.
```python
try:
    #WriteCSV(dir_,filename,soup)
    cd.WriteCondensedFmt(dir_,filename,soup,info)
    print dir_, filename, " -- collected."
```
where `WriteCSV` is the raw format and `WriteCondensedFmt` is condensed.
