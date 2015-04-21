# IcePick [![Circle CI](https://circleci.com/gh/teitei-tk/ice-pick.svg?style=svg)](https://circleci.com/gh/teitei-tk/ice-pick)
IcePick is a All in one Package library for easy Scraping

---

## Concept
* Lightweight Scraping Library 
* All in one Package library for easy Scraping

## Requirements
* Python 3.4 or later(not support 2.x)
* MongoDB

## Dependencies Libraries
* aiohttp
* beautifulsoup4
* pymongo >= 3.0
* nose

## Usage
Scraping Flow, 
```
Your Scraping Order(Order) -> Do Scraping(Picker) -> HTML Parse(Parser) -> Save in Database(Record)
```

## Example
get a my repository filenames

```python

import icePick

db = icePick.get_database('icePick_example', 'localhost')


class GithubRepoParser(icePick.Parser):
    def serialize(self):
        result = {
            "files": [],
        }

        for v in self.bs.find_all(class_="js-directory-link"):
            result['files'] += [v.text]
        return result


class GithubRepoRecord(icePick.Record):
    struct = icePick.Structure(files=list())

    class Meta:
        database = db


class GithubRepoOrder(icePick.Order):
    def parse(self, html):
        parser = GithubRepoParser(html)
        return parser.run()

    def save(self, result):
        record = GithubRepoRecord.new(result)
        return record.save()


def main():
    document = {
        'url': 'https://github.com/teitei-tk/ice-pick/tree/master',
        'ua': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
    }

    print('---download start---')
    order = GithubRepoOrder(document.get('url'), document.get('ua'))
    picker = icePick.Picker([order])
    picker.run()
    print("---finish---")

if __name__ == "__main__":
    main()
```

```
>>> import icePick
>>> db = icePick.get_database('icePick_example', 'localhost')
>>> class GithubRepoRecord(icePick.Record):
...     struct = icePick.Structure(files=list())
...     class Meta:
...         database = db
...
>>> records = GithubRepoRecord.find()
>>> records[0].files
['example', 'icePick', 'tests', 'LICENSE', 'README.md', 'circle.yml', 'requirements.txt']
>>>
```

## TODO
* Crawling
* Document

## LICENSE
* MIT

