import React from "react";

var Ask_Question = function(props) {

  var handleClick = function(event) {
    props.handleClick();
  }

  return(
    <button className="ask-question" onClick={handleClick}>?</button>
  )

};

export default Ask_Question