import React, { Component } from 'react'
import { TextField, Button, Grid, Typography } from "@material-ui/core";
import { Link } from "react-router-dom";
import {withRouter} from './withRouter';

class RoomJoinPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      roomCode: "",
      error: "",
    };
    this.handleRoomCode = this.handleRoomCode.bind(this);
    this.roomButtonClicked=this.roomButtonClicked.bind(this);
  }

  handleRoomCode = (e) => {
    this.setState({
      roomCode: e.target.value,
    });
  }

  roomButtonClicked(){
    const requestOptions={
      method:"POST",
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({
        code: this.state.roomCode,
      })
    };
    fetch('/api/join-room',requestOptions)
    .then((response)=>{
      if(response.ok){
        this.props.navigate(`/room/${this.state.roomCode}`);
      }
      else{
        this.setState({
          error: "ROOM NOT FOUND"
        })
      }
    }).catch((error)=>{
      console.log(error);
    });
    // console.log(this.state.roomCode)
  }

  render(){
  return (
    <div>
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <Typography component="h4" variant="h4">
            Join A Room
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <TextField
          error={this.state.error}
          label="Code"
          placeholder="Enter Room Code"
          value={this.state.roomCode}
          helperText={this.state.error}
          variant="outlined"
          onChange={this.handleRoomCode}
          />
        </Grid>
        <Grid item xs={12} align="center">
          <Button variant="contained" color="primary" onClick={this.roomButtonClicked}>ENTER ROOM</Button> 
        </Grid>
        <Grid item xs={12} align="center">
          <Button variant="contained" color="secondary" component={Link} to="/">BACK</Button>
        </Grid>
      </Grid>
    </div>
  )
  };
}

export default withRouter(RoomJoinPage)