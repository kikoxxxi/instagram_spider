# InstagramSpider
This is a Scrapy project to scrape Jacob's(My little boyfriend's boyfriend ∩ᵒ̴̶̷̤⌔ᵒ̴̶̷̤∩) shared information on [instagram](https://www.instagram.com/jacobbix/).
## Extracted data
This project extracts each shared infomation's detail url("original_url" as key name in database), combined with the respective total comments, image's url and so on. 
The crawler use MongoDB for storing data.
The extracted data in MongoDB looks like this:
```
{
    "_id" : ObjectId("5ab0d80ed3a94614cda221a3"),
    "original_url" : "https://www.instagram.com/p/BgUsi56Bgrv/?taken-by=jacobbix",
    "preview_like_count" : 44080,
    "type_name" : "GraphImage",
    "image_text" : "Swim w me",
    "comment_count" : 529,
    "image_url" : "https://scontent-lax3-1.cdninstagram.com/vp/6ba687381b91d4d5b84c20940055d6c1/5B33B256/t51.2885-15/e35/28433486_1804941946234678_4535244568450301952_n.jpg"
}
{
    "_id" : ObjectId("5ab0d810d3a94614cda221a5"),
    "original_url" : "https://www.instagram.com/p/BgNUJ1WBDfl/?taken-by=jacobbix",
    "preview_like_count" : 63463,
    "type_name" : "GraphSidecar",
    "image_text" : "@GAYTIMESMAG MARCH COVER ❤️",
    "comment_count" : 776,
    "image_url" : [ 
        "https://scontent-lax3-1.cdninstagram.com/vp/0bbd4d682a349ab49c6b4f20e16a5f45/5B32C700/t51.2885-15/e35/28435688_1689825057722352_599212693013921792_n.jpg", 
        "https://scontent-lax3-1.cdninstagram.com/vp/8e9d99cc5255d79e98632a278692fa17/5B37BE5C/t51.2885-15/e35/28752472_205151106898509_4557486997190475776_n.jpg"
    ]
}
```
## Running the spiders
`$ scrapy crawl jacobbix_spider`
