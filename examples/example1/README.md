# Example 1 

Given: 

Your configuration file is [config.yaml](config.yaml) with contents: <br />

```yaml
search:
  paths: # Where to search for notes
    - .
  filters: # Files to filter against
    - md
    - txt
any: false # Match any vs all topics, not yet implemented
nopause: false # If true, don't pause between matched topics
```

* You want to find topic headers containing the words _foo_ _bar_ and _baz_<br />
  ```bash
  bert.cheater find foo bar baz
  ```

* You want to find topic headers containing the words _fuzzy_ _wuzzy_<br />
  ```bash
  bert.cheater find fuzzy wuzzy
  ```