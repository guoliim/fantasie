# Fantasie backend API

This documentation uses bold italics like ***rawhash*** as the required parameter

## /api/list

Use this to retrieve the song list by different method

#### Method

`GET`
  
#### URL Params

|parameter|type|description|
|:---:|:---:|:---:|
|method|string|use "album" for randomizing by album|
|codec|string|"aac", "alac"|
|type|string| "Classical", "Popular", "Light", "Soundtrack"|
|title |string|just need contain, "Ballade"|
|artist|string|just need contain, "Abbado"|
|album|string|just need contain, "Goldberg"|
|composer|string|must equal, "Bach"|
|genre|string|must equal, "Classical"|
|year|int|must equal, "1984"|
|grouping|string|must equal, "Light"|
|country|string|"Chinese", "Korea", "Japanese", "Others"|

#### Success Response

an json array, like:
```json
[
  {
    "rawhash": "aee826bb672ad5991b7d3dc771841399"
  },
  {
    "rawhash": "52e5f5dfea67c3eb04f215be51c10ceb"
  },
  {
    "rawhash": "90b41f4df19c9ebbe012094d2a8014e0"
  },
  {
    "rawhash": "70e62d84bdbfd809171c1e53e1811add"
  },
  {
    "rawhash": "95c3657c3bde6177718e63b0bae99892"
  },
  {
    "rawhash": "66bd21767cbce39281a661e90096c631"
  },
  {
    "rawhash": "1c5fa61da2a936a15ee37e1f282172f4"
  },
  {
    "rawhash": "de4a8c77615d165e992a82bc6d8c0651"
  },
  {
    "rawhash": "08d5abbf29e9a81f4be7832c466b89dc"
  },
  {
    "rawhash": "f8343d1515d408155a7b03124f045644"
  }
]
```

--------------
## /api/meta

Use this to retrieve the song meta data by song's rawhash

#### Method

`GET`
  
#### URL Params

|parameter|type|description|
|:---:|:---:|:---:|
|***rawhash***|string|song identifier, like "e9d0098a4f7d0f3c50bf56bc8cde5fe2"|

#### Success Response

an json dictionary not array, like:
```json
{
  "title": "Polanaise - Tchaikovsky: Eugene Onegin, Op. 24",
  "artist": "Yuri Temirkanov: St. Petersburg Philharmonic Orchestra",
  "album": "Tchaikovsky: Symphony No. 6 \"Pathétique\", Etc.",
  "year": 1990,
  "genre": "Classical",
  "grouping": null,
  "track_n": 5,
  "track_t": 5,
  "disk_n": 1,
  "disk_t": 1,
  "fileurl": "/media/music/Yuri%20Temirkanov_%20St.%20Petersburg%20Philharmonic%20Orchestra/Tchaikovsky_%20Symphony%20No.%206%20_Path%C3%A9tique_%2C%20Etc_/05%20Polanaise%20-%20Tchaikovsky_%20Eugene%20Onegin%2C%20Op.%2024.m4a",
  "coverurl": "/static/covers/3c5e4a0dc14efe77cd5107caa0e47b2e.jpg",
  "rawhash": "e9d0098a4f7d0f3c50bf56bc8cde5fe2",
  "length": 255,
  "bitrate": 695665,
  "codec": "alac",
  "country": "Others",
  "composer": "Polanaise - Tchaikovsky",
  "cache": false
}
```

--------------
## /api/song_album_list

Use this to retrieve the entire album list by single song

#### Method

`GET`
  
#### URL Params

|parameter|type|description|
|:---:|:---:|:---:|
|***rawhash***|string|song identifier, like "58a453367a72a32026a7087331af01b0"|

#### Success Response

an json array, like:
```json
[
  {
    "rawhash": "58a453367a72a32026a7087331af01b0"
  },
  {
    "rawhash": "cba8c80376561fb393a3484f44c6930c"
  },
  {
    "rawhash": "c310577b3b3137fe32f999b0b7eeb92c"
  },
  {
    "rawhash": "d61ce40f93b88b617f2e1a8c67961947"
  },
  {
    "rawhash": "e9d0098a4f7d0f3c50bf56bc8cde5fe2"
  }
]
```

--------------
## /api/recommendation

Use this to retrieve the song list recommendation data

#### Method

`GET`
  
#### URL Params

None

#### Success Response

an json array, like:
```json
[
  {
    "refer": "/api/list?type=Popular",
    "name": "Popular",
  },
  {
    "refer": "/api/list?type=Classical",
    "name": "Classical",
  },
  {
    "refer": "/api/list",
    "name": "All"
  },
  {
    "refer": "/api/list?type=Soundtrack",
    "name": "Soundtrack",
  },
  {
    "refer": "/api/list?country=Chinese",
    "name": "Chinese",
  }
]
```
