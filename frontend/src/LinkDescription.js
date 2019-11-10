import React, { Component } from "react";
import magAfter from "./imgs/magAfter.png";
import magBefore from "./imgs/magBefore.png";
class LinkDescription extends Component {
  constructor(props) {
    super(props);
    this.handleFilter = this.handleFilter.bind(this);
  }

  handleFilter(filter) {
    if (filter === 2) {
      return (
        <div className="row">
          <div className="linkInfoLeft">
            <div className="liDiv">
              <a href={this.props.link3} target="_blank" className="hoverMag">
                <img src={magAfter} className="magAfter" alt="magAfter" />
              </a>
              <img src={magBefore} className="magBefore" alt="magBefore" />
            </div>
          </div>
          <div className="linkInfoRight">
            <p className="genText">
              Site: <br />
              {this.props.linkTitle3}
            </p>
          </div>
        </div>
      );
    }
    //photography
    if (filter === 1) {
      return (
        <div className="row">
          <div className="linkInfoLeft">
            <div className="liDiv">
              <a href={this.props.link2} target="_blank" className="hoverMag">
                <img src={magAfter} className="magAfter" alt="magAfter" />
              </a>
              <img src={magBefore} className="magBefore" alt="magBefore" />
            </div>
          </div>
          <div className="linkInfoRight">
            <p className="genText">
              Site: <br />
              {this.props.linkTitle2}
            </p>
          </div>
        </div>
      );
    } else {
      return (
        <div className="row">
          <div className="linkInfoLeft">
            <div className="liDiv">
              <a href={this.props.link1} target="_blank" className="hoverMag">
                <img src={magAfter} className="magAfter" alt="magAfter" />
              </a>
              <img src={magBefore} className="magBefore" alt="magBefore" />
            </div>
          </div>
          <div className="linkInfoRight">
            <p className="genText">
              Site: <br />
              {this.props.linkTitle1}
            </p>
          </div>
        </div>
      );
    }
  }
  render() {
    var output = this.handleFilter(this.props.filter);

    return <div className="toolComponentDiv">{output}</div>;
  }
}
export default LinkDescription;
