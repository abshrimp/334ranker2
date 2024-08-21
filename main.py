import chromedriver_binary
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
import time
import datetime
import json
import os
import traceback

timeline_body = {}
search_body = {}

def login_twitter(account, password, tel, driver):
    global timeline_body, search_body
    for _ in range(3):
        try:
            driver.get('https://x.com/i/flow/login')
            driver.maximize_window()
            element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "text")))
            time.sleep(1)

            cookie = {
                    'name': 'auth_token',
                    'value': password,
                    'domain': '.x.com',
                    'path': '/'
            }
            driver.add_cookie(cookie)
            time.sleep(1)
            driver.get('https://x.com')
            
            time.sleep(20)
            
            driver.get('https://x.com/home')
            time.sleep(20)
            
            for _ in range(5):
                for request in driver.requests:
                    if request.response:
                        if "Timeline" in request.url and "graphql" in request.url:
                            if request.body != b'':
                                timeline_body2 = json.loads(request.body)
                                time.sleep(0.5)
                                if "variables" in timeline_body2:
                                    timeline_body = timeline_body2
                                    print("set timeline_body")
                                    break
                            else:
                                timeline_body2 = request.params
                                time.sleep(0.5)
                                if "variables" in timeline_body2:
                                    timeline_body = timeline_body2
                                    timeline_body["variables"] = json.loads(timeline_body["variables"])
                                    timeline_body["features"] = json.loads(timeline_body["features"])
                                    print("set timeline_body")
                                    break
                if timeline_body != {}:
                    break
                time.sleep(0.5)

            
            driver.get('https://x.com/search?q=334&src=typed_query&f=live')
            time.sleep(20)
            
            for _ in range(5):
                for request in driver.requests:
                    if request.response:
                        if "SearchTimeline" in request.url and "graphql" in request.url:
                            if request.body != b'':
                                search_body2 = json.loads(request.body)
                                time.sleep(0.5)
                                if "variables" in search_body2:
                                    search_body = search_body2
                                    print("set search_body")
                                    break
                            else:
                                search_body2 = request.params
                                time.sleep(0.5)
                                if "variables" in search_body2:
                                    search_body = search_body2
                                    for key in search_body:
                                    	search_body[key] = json.loads(search_body[key])
                                    print("set search_body")
                                    break
                if search_body != {}:
                    break
                time.sleep(0.5)
        
        except Exception as e:
            traceback.print_exc()
        else:
            break


def TweetIdTime(id):
    epoch = ((id >> 22) + 1288834974657) / 1000.0
    d = datetime.datetime.fromtimestamp(epoch)
    return d

            
def make_ranking(dict, driver):
    now = datetime.datetime.now()
    time1 = datetime.datetime(now.year, now.month, now.day, 3, 34, 0)
    winner = ""
    users = []
    dict2 = []
    for item in dict:
        if item["text"] == "334" and item["user"]["id_str"] not in users:
            users.append(item["user"]["id_str"])
            time2 = TweetIdTime(int(item["id_str"]))
            res = (time2 - time1).total_seconds()
            if 0 <= res and res < 1:
                result = '{:.3f}'.format(res)
                if winner == "" or result == winner:
                    winner = result

                img_src = "https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png"
                if item["user"]["profile_image_url_https"] != "":
                    img_src = item["user"]["profile_image_url_https"]
                
                dict2.append([
                    img_src,
                    item["user"]["name"],
                    str(result),
                    item["source"],
                    item["id_str"],
                    "@" + item["user"]["screen_name"],
                    item["user"]["id_str"]
                ])

    print(str(dict2))

    

def get_334(driver):
    now = datetime.datetime.now()
    time1 = datetime.datetime(now.year, now.month, now.day, 3, 33, 59)
    time2 = datetime.datetime(now.year, now.month, now.day, 3, 34, 2)
    get_time = datetime.datetime(now.year, now.month, now.day, 3, 34, 3)
    while True:
        if get_time < datetime.datetime.now():
            driver.execute_script("""
window.data = "";
var url1 = 'https://api.twitter.com/1.1/search/';
var url2 = '.json?count=100&result_type=recent&q=334 since:""" + time1.strftime('%Y-%m-%d_%H:%M:%S_JST') + """ until:""" + time2.strftime('%Y-%m-%d_%H:%M:%S_JST') + """ -filter:retweets -filter:quote -from:rank334 -from:rank334_2';
var out = [];
var out2 = [];
var out3 = [];
var out4 = [];
var cookie = document.cookie.replaceAll(" ", "").split(";");
var token = "";
cookie.forEach(function (value) {
    let content = value.split('=');
    if (content[0] == "ct0") token = content[1];
})
let time1 = new Date()
time1.setHours(3);
time1.setMinutes(34);
time1.setSeconds(0);
time1.setMilliseconds(0);

function get_queryid(name, defaultId) {
    try {
        let queryids = webpackChunk_twitter_responsive_web;
        for (let i = 0; i < queryids.length; i++) {
            for (let key in queryids[i][1]) {
                try {
                    if (queryids[i][1][key].length === 1) {
                        let tmp = {};
                        queryids[i][1][key](tmp);
                        if (tmp.exports.operationName === name) return tmp.exports.queryId;
                    }
                } catch { }
            }
        }
        return defaultId;
    } catch {
        return defaultId;
    }
}

var data = arguments[0];
data.variables["cursor"] = "";
data.variables.seenTweetIds = [];
let queryid = get_queryid("HomeLatestTimeline", "02vsYHq98uLTwnNu2VF0Lg");
data.queryId = queryid;
var data2 = arguments[1];
data2.variables["cursor"] = "";
data2.variables["rawQuery"] = "334 -filter:retweets -filter:quote -from:rank334 -from:rank334_2 since:""" + time1.strftime('%Y-%m-%d_%H:%M:%S_JST') + """ until:""" + time2.strftime('%Y-%m-%d_%H:%M:%S_JST') + """"
let queryid2 = get_queryid("SearchTimeline", "KUnA_SzQ4DMxcwWuYZh9qg");
var count = 0;
//get_tweets();
//get_tweets2();
get_tweets3(data);
get_tweets4(data2);


function setheader(xhr) {
    xhr.setRequestHeader('Authorization', 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA');
    xhr.setRequestHeader('x-csrf-token', token);
    xhr.setRequestHeader('x-twitter-active-user', 'yes');
    xhr.setRequestHeader('x-twitter-auth-type', 'OAuth2Session');
    xhr.setRequestHeader('x-twitter-client-language', 'ja');
    xhr.withCredentials = true;
}

function get_tweets(max_id) {
    let xhr = new XMLHttpRequest();
    let url = max_id !== undefined ? url1 + "universal" + url2 + " max_id:" + max_id : url1 + "universal" + url2;
    xhr.open('GET', url);
    setheader(xhr);
    xhr.send();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            console.error("get1");
            if (xhr.status === 200) {
                try {
                    res = JSON.parse(xhr.responseText).modules;
                    if (res.length <= 0 || (max_id !== undefined && res.length <= 1)) final([]);
                    else {
                        if (max_id !== undefined) res.shift();
                        for (let i = 0; i < res.length; i++) {
                            let tweet = res[i].status.data;
                            tweet["index"] = parseInt(BigInt(tweet.id_str).toString(2).slice(0, -22), 2) + 1288834974657;
                            out.push(tweet);
                        }
                        get_tweets(out[out.length - 1].id_str);
                    }
                } catch (e) {
                    console.error(e);
                    final([]);
                }
            } else final([]);
        }
    }
}

function get_tweets2(max_id) {
    let xhr = new XMLHttpRequest();
    let url = max_id !== undefined ? url1 + "tweets" + url2 + " max_id:" + max_id : url1 + "tweets" + url2;
    xhr.open('GET', url);
    setheader(xhr);
    xhr.send();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            console.error("get2");
            if (xhr.status === 200) {
                try {
                    res = JSON.parse(xhr.responseText);
                    if ('statuses' in res) {
                        res = res.statuses;
                        if (res.length <= 0 || (max_id !== undefined && res.length <= 1)) final(out2);
                        else {
                            if (max_id !== undefined) res.shift();
                            for (let i = 0; i < res.length; i++) {
                                let tweet = res[i];
                                tweet["index"] = parseInt(BigInt(tweet.id_str).toString(2).slice(0, -22), 2) + 1288834974657;
                                out2.push(res[i]);
                            }
                            get_tweets2(out2[out2.length - 1].id_str);
                        }
                    } else final(out2);
                } catch (e) {
                    console.error(e);
                    final(out2);
                }
            } else final(out2);
        }
    }
}

function get_tweets3(d) {
    try {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'https://x.com/i/api/graphql/' + queryid + '/HomeLatestTimeline');
        setheader(xhr);
        xhr.setRequestHeader('content-type', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                console.error("get3");
                if (xhr.status === 200) {
                    try {
                        var flag = true;
                        let entries = JSON.parse(xhr.responseText).data.home.home_timeline_urt.instructions[0].entries;
                        for (let i = 0; i < entries.length; i++) {
                            if (!entries[i].entryId.includes("promoted") && !entries[i].entryId.includes("cursor")) {
                                try {
                                    if (entries[i].entryId.includes("home")) var res = entries[i].content.items[0].item.itemContent.tweet_results.result;
                                    else var res = entries[i].content.itemContent.tweet_results.result;
                                    if ("tweet" in res) res = res.tweet;
                                    let legacy = res.legacy;
                                    if (new Date(legacy.created_at) < time1) {
                                        if (entries[i].entryId.includes("home")) continue;
                                        else {
                                            flag = false;
                                            final(out3);
                                            break;
                                        }
                                    }
                                    legacy["text"] = legacy.full_text;
                                    if (legacy.text != "334") continue;
                                    legacy["source"] = res.source;
                                    legacy["index"] = parseInt(BigInt(legacy.id_str).toString(2).slice(0, -22), 2) + 1288834974657;
                                    legacy["user"] = res.core.user_results.result.legacy;
                                    legacy.user["id_str"] = legacy.user_id_str;
                                    out3.push(legacy);
                                    continue;
                                } catch (e) {
                                    console.error(e);
                                }
                            }
                            if (entries[i].entryId.includes("bottom")) {
                                let data3 = Object.assign({}, data);
                                data3.variables.cursor = entries[i].content.value;
                                flag = false;
                                get_tweets3(data3);
                                break;
                            }
                        }
                        if (flag) final(out3);
                    } catch (e) {
                        console.error(e);
                        final(out3);
                    }
                } else final(out3);
            }
        }
        xhr.send(JSON.stringify(d));
    } catch (e) {
        console.error(e);
        final(out3);
    }
}

function get_tweets4(d) {
    try {
        let param = "?" + Object.entries(d).map((e) => {
            return `${e[0].replaceAll("%22", "")}=${encodeURIComponent(JSON.stringify(e[1]))}`
        }).join("&")
        var xhr = new XMLHttpRequest();
        xhr.open('GET', 'https://x.com/i/api/graphql/' + queryid2 + '/SearchTimeline' + param);
        setheader(xhr);
        xhr.setRequestHeader('content-type', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                console.error("get4");
                if (xhr.status === 200) {
                    try {
                        var flag = true;
                        let instructions = JSON.parse(xhr.responseText).data.search_by_raw_query.search_timeline.timeline.instructions;
                        var flag2 = true;
                        loop: for (let j = 0; j < instructions.length; j++) {
                            if ("entries" in instructions[j]) var entries = instructions[j].entries;
                            else if ("entry" in instructions[j]) var entries = [instructions[j].entry];
                            else continue;
                            for (let i = 0; i < entries.length; i++) {
                                if (!entries[i].entryId.includes("promoted") && !entries[i].entryId.includes("cursor")) {
                                    try {
                                        flag2 = false;
                                        var res = entries[i].content.itemContent.tweet_results.result;
                                        if ("tweet" in res) res = res.tweet;
                                        let legacy = res.legacy;
                                        if (new Date(legacy.created_at) < time1) {
                                            if (entries[i].entryId.includes("home")) continue;
                                            else {
                                                flag = false;
                                                final(out4);
                                                break loop;
                                            }
                                        }
                                        legacy["text"] = legacy.full_text;
                                        if (legacy.text != "334") continue;
                                        legacy["source"] = res.source;
                                        legacy["index"] = parseInt(BigInt(legacy.id_str).toString(2).slice(0, -22), 2) + 1288834974657;
                                        legacy["user"] = res.core.user_results.result.legacy;
                                        legacy.user["id_str"] = legacy.user_id_str;
                                        out4.push(legacy);
                                        continue;
                                    } catch (e) {
                                        console.error(e);
                                    }
                                }
                                if (entries[i].entryId.includes("bottom")) {
                                    let data3 = Object.assign({}, data2);
                                    data3.variables.cursor = entries[i].content.value;
                                    flag = false;
                                    if (flag2) final(out4);
                                    else get_tweets4(data3);
                                    break loop;
                                }
                            }
                        }
                        if (flag) final(out4);
                    } catch (e) {
                        console.error(e);
                        final(out4);
                    }
                } else final(out4);
            }
        }
        xhr.send();
    } catch (e) {
        console.error(e);
        final(out4);
    }
}

function final(out6) {
    out = out.concat(out6);
    count++;
    if (count < 2) return;
    let out5 = []
    let ids = [];
    out.sort((a, b) => a.index - b.index);
    for (let i = 0; i < out.length; i++) {
        if (!ids.includes(out[i].id_str)) {
            out5.push(out[i]);
            ids.push(out[i].id_str);
        }
    }
    window.data = out5;
    window.data2 = JSON.stringify(out5);
}
            """, timeline_body, search_body)
            while True:
                time.sleep(0.01)
                res = driver.execute_script("return window.data")
                if res != "":
                    res2 = driver.execute_script("return window.data2")
                    #response = requests.post(os.environ['GAS_URL'], data=json.dumps({'data': res2}))
                    make_ranking(res, driver)
                    break
            break
        time.sleep(0.01)


def start():
    for _ in range(3):
        try:
            options=Options()
            #options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-gpu")
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-http2')
            driver = webdriver.Chrome(options = options)
            
        except Exception as e:
            traceback.print_exc()
        else:
            break

    login_twitter("rank334", os.environ['PASS'], os.environ['TEL'], driver)
    get_334(driver)
         
start()
            
