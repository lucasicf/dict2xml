Dict2XML
==============================

Python tool useful to convert a JSON-style dictionary element to a XML document.


How? Show me...
------------------------------

### Basic example

```python
from dict2xml import dict2XML
json = {'street': {
    'name': '4th street',
    'city': 'Rio de Janeiro',
    'dwellers': '200'
}}
print dict2XML(json)
```
gives:
```xml
<?xml version="1.0" ?>
<street>
  <city>Rio de Janeiro</city>
  <dwellers>200</dwellers>
  <name>4th Street</name>
</street>
```

Notice that a python dictionary doesn't record the order of its keys, therefore there is a feature to order your data when it matters.

```python
json = {'street': {
    '1__name': '4th street',
    '2__city': 'Rio de Janeiro',
    '3__dwellers': '200'
}}
print dict2XML(json)
```
gives:
```xml
<?xml version="1.0" ?>
<street>
  <name>4th Street</name>
  <city>Rio de Janeiro</city>
  <dwellers>200</dwellers>
</street>
```

You can also generate it with no indentation or linebreaks...

```python
print dict2XML(json, indent=False)
```
gives:
```xml
<?xml version="1.0" ?><street><name>4th Street</name><city>Rio de Janeiro</city><dwellers>200</dwellers></street>
```

... or encoded with UTF-8.

```python
json = {'street': {
    u'1__name': u'4th street',
    u'2__cíty': u'Río de Janêiro',
    u'3__dwéllers': u'200'
}}
print dict2XML(json, utf8=True)
```
gives:
```xml
<?xml version="1.0" encoding="utf-8"?>
<street>
  <name>4th Street</name>
  <cíty>Río de Janêiro</cíty>
  <dwéllers>200</dwéllers>
</street>
```

### Nested dictionaries

```python
from dict2xml import dict2XML
json = {'street': {
    '1__name': '4th street',
    '2__city': 'Rio de Janeiro',
    '3__dwellers': {
        '1__dweller1': {
            'name': 'Lucas',
            'age': '23'
        },
        '2__dweller2': {
            'name': 'Renata',
            'age': '25'
        },
        '3__dweller3': {
            'name': 'Rafael',
            'age': '55'
        }
    }
}}
print dict2XML(json)
```
gives:
```xml
<?xml version="1.0" ?>
<street>
  <name>4th Street</name>
  <city>Rio de Janeiro</city>
  <dwellers>
    <dweller1>
      <age>23</age>
      <name>Lucas</name>
    </dweller1>
    <dweller2>
      <age>25</age>
      <name>Renata</name>
    </dweller2>
    <dweller3>
      <age>55</age>
      <name>Rafael</name>
    </dweller3>
  </dwellers>
</street>
```

### Lists

Useful to create multiple entries of an element. Lists are ordered, there's no needing to use any extra feature.

```python
from dict2xml import dict2XML
json = {'street': {
    '1__name': '4th street',
    '2__city': 'Rio de Janeiro',
    '3__dwellers': {
        'dweller': [
            {
                '1__name': 'Lucas',
                '2__age': '23'
            },
            {
                '1__name': 'Renata',
                '2__age': '25'
            },
            {
                '1__name': 'Rafael',
                '2__age': '55'
            }
        ]
    }
}}
print dict2XML(json)
```
gives:
```xml
<?xml version="1.0" ?>
<street>
  <name>4th Street</name>
  <city>Rio de Janeiro</city>
  <dwellers>
    <dweller>
      <name>Lucas</name>
      <age>23</age>
    </dweller>
    <dweller>
      <name>Renata</name>
      <age>25</age>
    </dweller>
    <dweller>
      <name>Rafael</name>
      <age>55</age>
    </dweller>
  </dwellers>
</street>
```

### Element attributes

Easy to do. Instead of passing the content of an element as the value of the key, pass a 2-tuple in which the second element is the content. The first will be the attributes. For the lists, pass individual set of attributes for each value of the list.

```python
from dict2xml import dict2XML
json = {'street': {
    '1__name': '4th street',
    '2__city': ({'country': 'Brazil'}, 'Rio de Janeiro'),
    '3__dwellers': {
        'dweller': [
            ({'id': '1'}, {
                '1__name': 'Lucas',
                '2__age': '23'
            }),
            ({'id': '2'}, {
                '1__name': 'Renata',
                '2__age': '25'
            }),
            ({'id': '3'}, {
                '1__name': 'Rafael',
                '2__age': '55'
            })
        ]
    }
}}
print dict2XML(json)
```
gives:
```xml
<?xml version="1.0" ?>
<street>
  <name>4th Street</name>
  <city country="Brazil">Rio de Janeiro</city>
  <dwellers>
    <dweller id="1">
      <name>Lucas</name>
      <age>23</age>
    </dweller>
    <dweller id="2">
      <name>Renata</name>
      <age>25</age>
    </dweller>
    <dweller id="3">
      <name>Rafael</name>
      <age>55</age>
    </dweller>
  </dwellers>
</street>
```


Install
------------------------------

Get it by git...
```
git clone git://github.com/lucasicf/dict2xml.git
cd dict2xml
```

... or download the zip offered by GitHub.
```
wget https://github.com/lucasicf/dict2xml/archive/master.zip
unzip master.zip -d dict2xml
cd dict2xml/dict2xml-master
```

Run the installer.
```
python setup.py install
```

Optionally, run the tests:
```
python runtests.py
```
