var percentage;
var link1;
var link2;
var link3;
chrome.runtime.sendMessage({ from: "content" });
chrome.runtime.onMessage.addListener(function(msg, sender, sendResponse) {
  if (msg.from == "background" && msg.event == "true") {
    percentage = msg.percentage;
    link1 = msg.link1;
    link2 = msg.link2;
    link3 = msg.link3;
    console.log(percentage, link1, link2, link3);
    const eventDiv = document.createElement("div");
    eventDiv.id = "myDivIdAct";
    eventDiv.style.position = "fixed";
    eventDiv.style.margin = "0px";
    eventDiv.style.padding = "0px";
    eventDiv.style.bottom = "-290px";
    eventDiv.style.right = "0px";
    eventDiv.style.transition = "bottom 1.2s";
    eventDiv.style.zIndex = "2147483647";
    eventDiv.style.width = "400px";
    eventDiv.style.height = "290px";
    eventDiv.style.opacity = "0.9";
    eventDiv.style.backgroundColor = "#1E1E1E";
    eventDiv.innerHTML = `<iframe id="actNow"style="height:100%; width:100%"></iframe><link href="https://fonts.googleapis.com/css?family=Roboto:300&display=swap" rel="stylesheet"/>
            <div-z style="position:absolute; top:12px; right:18px; ">  
                <h6-z id="unique" style="cursor:pointer; transition: color 0.3s; font-family: 'Roboto', sans-serif; font-size: 30px; padding:0px; margin:0px; color:#ffffff;" onmouseout="this.style.color='#ffffff'" onmouseover="this.style.color='#ff6464'">x</h6-z>
            </div-z>`;
    document.body.appendChild(eventDiv);
    const iframe = document.getElementById("actNow");
    iframe.src = chrome.extension.getURL("index.html");
    iframe.frameBorder = 0;

    eventDiv.querySelector("h6-z").addEventListener("click", () => {
      eventDiv.remove();
    });
  } else if (msg.from == "reactapp") {
    console.log("sendmsadddddddddddddddessagee:");
    sendResponse({
      from: "content",
      percentage: percentage,
      link1: link1,
      link2: link2,
      link3: link3
    });
    document.getElementById("myDivIdAct").style.bottom = "0px";
  } else {
    console.log("Act Now App: Nothing Found");
  }
});
