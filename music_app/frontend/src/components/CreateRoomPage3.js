import React from "react";
// import Button from "@material-ui/core/Button";
// import Grid from "@material-ui/core/Grid";
// import Typography from "@material-ui/core/Typography";
// import TextField from "@material-ui/core/TextField";
// import FormHelperText from "@material-ui/core/FormHelperText";
// import FormControl from "@material-ui/core/FormControl";
// import { Link } from "react-router-dom";
// import Radio from "@material-ui/core/Radio";
// import RadioGroup from "@material-ui/core/RadioGroup";
// import FormControlLabel from "@material-ui/core/FormControlLabel";

const CreateRoomPage3 = () => {


  return (
    <div>
    <div>CREATE A ROOM</div>
    <div>guest control of playback</div>
    <div>
        <input type="radio" name="guestCanPause" value="true" >PLay/Pause</input>
        <input type="radio" name="guestCanPause" value="false" >NO CONTROL</input>
    </div>
    <div>
        <input type="text" name="votesToSkip" value="2" >Votes to skip</input>
    </div>
    <button> Create room</button>
    <button> back </button>
      </div>
  )
}

export default CreateRoomPage3