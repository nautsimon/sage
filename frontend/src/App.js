/* global chrome */

import React, { Component } from "react";

import LinkDescription from "./LinkDescription";
import icon from "./imgs/logoFS.png";
import "./App.css";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      filter: 0,
      percentage: "",
      link1: "",
      link2: "",
      link3: "",
      linkTitle1: "",
      linkTitle2: "",
      linkTitle3: ""
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
              link3: response.link3,
              linkTitle1: response.linkTitle1,
              linkTitle2: response.linkTitle2,
              linkTitle3: response.linkTitle3
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
        link3: data.link3,
        linkTitle1: data.linkTitle1,
        linkTitle2: data.linkTitle2,
        linkTitle3: data.linkTitle3
      });
    });
  }
  handleFilter(filterNum) {
    this.setState({ filter: filterNum });
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
          Here are some other articles that could provide more insight on this
          topic.
        </p>
        <div className="row">
          <div className="tri center" onClick={() => this.handleFilter(0)}>
            <p
              style={{
                filter: this.state.filter === 0 ? "blur(0px)" : "blur(1px)"
              }}
              className="triText"
            >
              Insight 1
            </p>
          </div>

          <div
            className="tri center borders"
            onClick={() => this.handleFilter(1)}
          >
            <p
              style={{
                filter: this.state.filter === 1 ? "blur(0px)" : "blur(1px)"
              }}
              className="triText"
            >
              Insight 2
            </p>
          </div>

          <div className="tri center" onClick={() => this.handleFilter(2)}>
            <p
              style={{
                filter: this.state.filter === 2 ? "blur(0px)" : "blur(1px)"
              }}
              className="triText"
            >
              Insight 3
            </p>
          </div>
        </div>
        <LinkDescription
          filter={this.state.filter}
          link1={this.state.link1}
          link2={this.state.link2}
          link3={this.state.link3}
          linkTitle1={this.state.linkTitle1}
          linkTitle2={this.state.linkTitle2}
          linkTitle3={this.state.linkTitle3}
        />
      </div>
    );
  }
}
export default App;
