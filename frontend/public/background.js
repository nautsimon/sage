var contentTabId;
// add geolocation

// add organization logos to the banner
var eventResp = {
  isEvent: "false",
  percentage: "",
  link1: "",
  link2: "",
  link3: ""
};
let getUrl = function() {
  return new Promise((resolve, reject) => {
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
      var domain = tabs[0].url;
      resolve(domain);
    });
  });
};
let getApi = function(pageUrl) {
  // var pageUrl = pageUrl;
  // return new Promise(function(resolve, reject) {
  //   var percentage = "94";
  //   var link1 = "https://pornhub.com";
  //   var link2 = "https://twitter.com";
  //   var link3 = "https://google.com";
  //   eventResp = {
  //     isEvent: "true",
  //     percentage: percentage,
  //     link1: link1,
  //     link2: link2,
  //     link3: link3
  //   };
  //   console.log(eventResp);
  //   resolve(eventResp);
  // });
  // url = "https://sage-258600.appspot.com/getcheck/"
  // url = "http://localhost:5000/getcheck/";
  //  linkTitle1: "cumm",
  //             linkTitle2: "cumm",
  //             linkTitle3: "cummcumm",
  //             linkPerc1: "98",
  //             linkPerc2: "91",
  //             linkPerc3: "92"
  var pageUrl = pageUrl;
  console.log("page url:", pageUrl);
  var xhr = new XMLHttpRequest(),
    method = "POST",
    url = "http://localhost:5000/getcheck/";
  return new Promise(function(resolve, reject) {
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        response = JSON.parse(xhr.responseText);
        if (response.percentage != "fail") {
          eventResp = {
            isEvent: "true",
            percentage: response.percentage,
            link1: response.link1,
            link2: response.link2,
            link3: response.link3,
            linkTitle1: response.linkTitle1,
            linkTitle2: response.linkTitle2,
            linkTitle3: response.linkTitle3,
            linkPerc1: "2",
            linkPerc2: "2",
            linkPerc3: "2"
          };
          resolve(eventResp);
        } else {
          eventResp = {
            isEvent: "false",
            percentage: "",
            link1: "",
            link2: "",
            link3: "",
            linkTitle1: "",
            linkTitle2: "",
            linkTitle3: "",
            linkPerc1: "",
            linkPerc2: "",
            linkPerc3: ""
          };
          console.log("Sage: nothing found");
          resolve(eventResp);
        }
      }
    };
    xhr.open(method, url);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(
      JSON.stringify({
        url: pageUrl
      })
    );
  });
};
let sendMessage = function(msg, sender, result) {
  var response = eventResp;
  return new Promise((resolve, reject) => {
    chrome.tabs.sendMessage(contentTabId, {
      from: "background",
      percentage: response.percentage,
      event: response.isEvent,
      link1: response.link1,
      link2: response.link2,
      link3: response.link3,
      linkTitle1: response.linkTitle1,
      linkTitle2: response.linkTitle2,
      linkTitle3: response.linkTitle3,
      linkPerc1: response.linkPerc1,
      linkPerc2: response.linkPerc2,
      linkPerc3: response.linkPerc3
    });
    resolve("message sent");
  });
};
chrome.runtime.onMessage.addListener(function(msg, sender) {
  if (msg.from == "content" || msg.from == "reactapp") {
    contentTabId = sender.tab.id;
    getUrl()
      .then(result => {
        return getApi(result);
      })
      .then(() => {
        return sendMessage(msg, sender);
      })
      .then(result => {
        console.log(result);
      });
  }
});
