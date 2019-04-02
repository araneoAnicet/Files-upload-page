## Images storing service

# REQUIRED PRE-INSTALLED
'''bash
    flask
    flask_cors
    flask_sqlalchemy
    flask_bootstrap
    flask_restful
    werkzeug

'''


## All images
`api/images`
method: **GET**

***Response***
`200`

'''json
{
    "images": [
        {
            "id": image_1.id,
            "name": "image_1 name",
            "posted": "year-month-day hour minute second",
            "folder": "image_1 folder"
        },
        {
            "id": image_2.id,
            "name": "image_2 name",
            "posted": "year-month-day hour minute second",
            "folder": "image_2 folder"
        },
        ...
    ],
    "status": "OK"
}

 '''

## Image by hash

`api/images/IMAGE_HASH`
method: **GET**
description: Returns the information about searched image

***Response***
`200`

'''json
{
    "id": image.id,
    "name": "image_name",
    "posted": "year-month-day hour minute second",
    "folder": "image folder",
    "status": "OK"
}
'''

method: **DELETE**

***Response***
`200`

'''json
{
    "id": image.id,
    "name": "image_name",
    "posted": "year-month-day hour minute second",
    "folder": "image folder",
    "status": "OK"
}
'''


## Upload new image

`api/add/YOUR_FOLDER_NAME`
method: **POST**
description: Returns the information of uploaded file(s)

***Response***
`200`

'''json
{
    "images": [
        {
             "id": image_1.id,
            "name": "image_1 name",
            "posted": "year-month-day hour minute second",
            "folder": "image_1 folder",
            "hash": "image_1 hash"
        },
        {
             "id": image_2.id,
            "name": "image_2 name",
            "posted": "year-month-day hour minute second",
            "folder": "image_2 folder",
            "hash": "image_2 hash"
        },
        ...
    "status": "OK"
    ]
}
'''

***Response***
`404`

'''json
{
    "status": "No Files"
}
'''