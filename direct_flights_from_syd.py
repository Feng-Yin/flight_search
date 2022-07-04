# -*- coding: UTF-8 -*-
import requests
import json
import datetime
import matplotlib.pyplot as plt
import datetime


def next_weekday(weeks, weekday):
    today = datetime.date.today()
    days_ahead = (weekday - today.weekday()) % 7
    return today + datetime.timedelta(days=days_ahead, weeks=weeks)

fromCity = "SYD"
toCities = {
    "XMN": 3,  # every Thursday
    "SHA": 2,  # every Wednesday
    "CAN": 2,  # every Wednesday
}
total_weeks = 15
namesMap = {"SYD": "悉尼", "XMN": "厦门", "SHA": "上海", "CAN": "广州"}

url = "https://www.iwofly.cn/api/flight/search"
headers = {"Content-Type": "application/json"}
for toCity, weekday in toCities.items():
    print("==============================================================")
    dates = []
    prices = []
    for week in range(total_weeks):
        fromDate = next_weekday(week, weekday)
        fromDateStr = fromDate.strftime("%Y%m%d")
        payload = json.dumps(
            {
                "adultNumber": 2,
                "childNumber": 1,
                "infantNumber": 0,
                "cabinGrade": "Y",
                "fromCity": fromCity,
                "toCity": toCity,
                "fromDate": fromDateStr,
                "retDate": "",
                "tripType": "1",
                "currency": "CNY",
                "randomSeed": "GVeK8TaDfHwiFhOBj+1LUEQTfNLg20N8usXK22x6fII=",
                "upstreamInfo": {"name": "iwoflyCN", "subSite": "cn"},
            }
        )
        response = requests.post(url, headers=headers, data=payload)
        # dump the response in a human readable format for debugging
        # print(json.dumps(json.loads(response.text), indent=4, sort_keys=True))

        if response.status_code == 200:
            respJson = response.json()
            routings = respJson.get("routings")
            found = False
            for routing in routings:
                if routing.get("transit") != 0:
                    continue
                adultPrice = routing.get("adultTotalPrice")
                kidPrice = routing.get("childTotalPrice")
                totalPrice = adultPrice * 2 + kidPrice
                print(
                    f"{fromDateStr} form {namesMap[fromCity]} to {namesMap[toCity]}: 成人:{adultPrice} 小孩:{kidPrice} 共计:{totalPrice}"
                )
                found = True
                dates.append(fromDate)
                prices.append(totalPrice)
            if not found:
                print(
                    f"{fromDateStr} form {namesMap[fromCity]} to {namesMap[toCity]}: 无直航"
                )

    plt.plot(dates, prices, "o-", label=toCity)
    plt.xticks(rotation=45)
    plt.gca().yaxis.set_major_formatter(
        plt.matplotlib.ticker.StrMethodFormatter("{x:,}")
    )
    plt.tight_layout()
    for x, y in zip(dates, prices):
        plt.text(x, y, "{:,}".format(y), rotation=45)
plt.legend()
# set title
plt.title(f"{fromCity} -> China")
plt.show()

