## LNBITS SETTINGS

LNBITS_BASE_URL = "https://legend.lnbits.com"
LNBITS_ADMIN_KEY = "<YOUR_LNBITS_ADMIN_KEY>"

## LNTXBOT SETTINGS
LNTXBOT_BASE_URL = "https://lntxbot.com"
LNTXBOT_API_KEY = "<YOUR_LNTXBOT_FULLAPI_KEY>"

LNURL_TITLE = "عیدت مبارک {} جان!"
IMAGE_TEXT = "برای {} جان! عیدت مبارک"
REWARD = 10000
URL = {
    "create_lnurl": 
    {
        "lnbits": "/withdraw/api/v1/links",
        "lntxbot": "/generatelnurlwithdraw"
    }
}

## IMAGE SETTINGS

TEMPLATES = {
    "dark": "templates/template-dark.png",
    "light": "templates/template-light.png"
}
LOGO = "templates/lightning_logo.png"
LOGO_SIZE = (60, 60)