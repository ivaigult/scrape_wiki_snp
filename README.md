# Scrape wiki S&P

Scrapes Wikipedia pages to get S&P indices components.

## Usage

To get S&P 500 components, run:

```
python -m scrape_wiki_snp https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
```

This will print the list of S&P 500 components and historical changes in .yaml format.

For S&P 400:

```
python -m scrape_wiki_snp https://en.wikipedia.org/wiki/List_of_S%26P_400_companies
```

For S&P 600:

```
python -m scrape_wiki_snp https://en.wikipedia.org/wiki/List_of_S%26P_600_companies
```
