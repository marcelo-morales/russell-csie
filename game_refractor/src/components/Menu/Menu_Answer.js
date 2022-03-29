import React from "react";

function Menu_Answer(props) {

  var handleChange = function(event) {
    event.preventDefault();
    var newIndex = event.target.value;
    props.handleChange(newIndex);
  }

  var options = props.answerMenu.map(function(answer, index){
    return <option value={index} key={index}>{answer}</option>
  });

  return(
    <div className="menu-answer">
      <select id="menu-answer" value={props.menuIndex} onChange={handleChange}>
        {options}
      </select>
    </div>
  )
};

export default Menu_Answer