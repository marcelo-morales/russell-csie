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
          <h1>Name:</h1>
          {/* <p>Gender:</p>
          <p>House:</p>
          <p>Ancestry:</p>
          <p>Eye colour:</p>
          <p>Hair colour:</p> */}
        </div>
        <div className="field-values">
          <h1>{props.character.name}</h1>
          {/* <p>{props.character.gender}</p>
          <p>{props.character.house}</p>
          <p>{props.character.ancestry}</p>
          <p>{props.character.eyeColour}</p>
          <p>{props.character.hairColour}</p> */}
        </div>
        <div className="card-overlay" style={{display: styleOverlay}}>
          <img src={redCross} />
        </div> 
      </div>    
    </div>
  );
}

export default Card;