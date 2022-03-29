import React from "react";

import redCross from "../../assets/red_cross.png";

function Card(props) {

  var styleOverlay = (props.hide) ? "block" : "none";
  return (
    <div className="card">
      <div className="pic">
        <img src={props.character.image}/>
      </div>
      <div className="details">
        <div className="field-names">
          <p>Name:</p>
          <p>Gender:</p>
          <p>House:</p>
          <p>Ancestry:</p>
          <p>Eye colour:</p>
          <p>Hair colour:</p>
        </div>
        <div className="field-values">
          <p>{props.character.name}</p>
          <p>{props.character.gender}</p>
          <p>{props.character.house}</p>
          <p>{props.character.ancestry}</p>
          <p>{props.character.eyeColour}</p>
          <p>{props.character.hairColour}</p>
        </div>
        <div className="card-overlay" style={{display: styleOverlay}}>
          <img src={redCross} />
        </div> 
      </div>    
    </div>
  );
}

export default Card;