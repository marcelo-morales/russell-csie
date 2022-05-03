import React from "react";

function Notification(props) {

  return(
    <div>
    <br></br>
    <br></br>
    <br></br>
    <h2 className="notification">{props.children}</h2>
    </div>
  )

};

export default Notification;