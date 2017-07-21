
# How to Setup a Test/Dev Instance

Demo depends on two things

1. a running instance of [digcoll_retriever](https://github.com/uchicago-library/digcoll_retriever) on localhost:5000
2. mvol files for mvol-0001-0003-0000. There must be tif files and a dc.xml file that looks like

```
<metadata>
    <title>This is a title</title>
    <date>2017</date>
    <description>This is a description</description>
    <identifier>mvol-0001-00003-0000</identifier>
</metadata>
```
3. running python manage.py load_new_issue http://localhost:5000/ ../testdata/import_data.json

The import data.json file should look like this:

```
[
{
    "identifier": "mvol-0001-0003-0000",
    "metadata":"mvol-0001-0003-0000/metadata",
    "pages": [
        "mvol-0001-0003-0000_0001",
        "mvol-0001-0003-0000_0002",
        "mvol-0001-0003-0000_0003",
        "mvol-0001-0003-0000_0004",
        "mvol-0001-0003-0000_0005",
        "mvol-0001-0003-0000_0006",
        "mvol-0001-0003-0000_0007",
        "mvol-0001-0003-0000_0008",
        "mvol-0001-0003-0000_0009",
        "mvol-0001-0003-0000_0010",
        "mvol-0001-0003-0000_0011",
        "mvol-0001-0003-0000_0012",
        "mvol-0001-0003-0000_0013",
        "mvol-0001-0003-0000_0014",
        "mvol-0001-0003-0000_0015"
    ]
}
]
```

4. run python manage.py createsuperuser and enter the username and admin you want in the relevant field request. Remember the username and password you enter: you will need them later.


5. running python manage.py runserver

6. access the admin interface via http://localhost:5000/admin

7. run demo by going to http://localhost:5000

Enter "Cap" in the search box and click Search or hit Enter key

8. Click on the volume information link to view a full page view of the matching Issue