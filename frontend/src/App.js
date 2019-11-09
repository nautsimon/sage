/* global chrome */

import React, { Component } from "react";

import magAfter from "./imgs/magAfter.png";
import magBefore from "./imgs/magBefore.png";
import icon from "./imgs/logoFS.png";
import "./App.css";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      percentage: "",
      link1: "",
      link2: "",
      link3: ""
    };
  }

  componentDidMount() {
    let getInfo = function() {
      return new Promise(function(resolve, reject) {
        chrome.tabs.query({ active: true, currentWindow: true }, function(
          tabs
        ) {
          chrome.tabs.sendMessage(tabs[0].id, { from: "reactapp" }, function(
            response
          ) {
            var data = {
              percentage: response.percentage,
              link1: response.link1,
              link2: response.link2,
              link3: response.link3
            };
            resolve(data);
          });
        });
      });
    };
    getInfo().then(data => {
      return this.setState({
        percentage: data.percentage,
        link1: data.link1,
        link2: data.link2,
        link3: data.link3
      });
    });
  }

  render() {
    return (
      <div className="modalBody">
        <div className="row paddingTop">
          <div className="left">
            <img className="icon" src={icon} alt="icon" />
          </div>
          <div className="right">
            <div className="percentDiv">
              <p className="percText">{this.state.percentage}%</p>
            </div>
          </div>
        </div>
        <div className="borderBottom">
          <p className="genText paddingBottom">
            Caution: Sage detected that there is a {this.state.percentage}%
            probability that this site contains fallacious information.
          </p>
        </div>
        <br />
        <p className="genText negPad">
          Here are some Sage verified articles that could provide more info on
          this topic.
        </p>
        <div className="row">
          <div className="tri">
            <div className="liDiv">
              <a href="https://https.pornhub.com/" className="hoverMag">
                <img src={magAfter} className="magAfter" alt="magAfter" />
              </a>
              <img src={magBefore} className="magBefore" alt="magBefore" />
            </div>
          </div>
          <div className="tri">
            <div className="liDiv">
              <a href="https://https.pornhub.com/" className="hoverMag">
                <img src={magAfter} className="magAfter" alt="magAfter" />
              </a>
              <img src={magBefore} className="magBefore" alt="magBefore" />
            </div>
          </div>
          <div className="tri">
            <div className="liDiv">
              <a href="https://https.pornhub.com/" className="hoverMag">
                <img src={magAfter} className="magAfter" alt="magAfter" />
              </a>
              <img src={magBefore} className="magBefore" alt="magBefore" />
            </div>
          </div>
        </div>
      </div>
    );
  }
}
export default App;
