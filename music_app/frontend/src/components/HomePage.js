import React,{Component, useState,useEffect} from "react";
import { Grid, Button, ButtonGroup, Typography } from "@material-ui/core";
import {Link} from "react-router-dom";
import { Navigate } from 'react-router-dom';

function HomePage() {
    const initialState = {
      roomCode:null,
    }
  // if user is in a room and goes to home page then he gets automatically redirected to that room again
  // for this lifecycle method componentdidmount is used
// componentdidmount means component just rendered for the first time on screen
  // async componentDidMount(){
  //   fetch('/api/user-in-room').then(
  //     (response) => response.json()
  //   ).then((data)=>{
  //     this.setState({
  //       roomCode: data.Code,
  //     })
  //   });

  const[roomCodeData,setRoomCodeData]=useState(initialState)
  useEffect(()=>{
    fetch('/api/user-in-room').then(
      response => response.json()
    ).then(data=>{
      setRoomCodeData({
        ...roomCodeData,
        roomCode: data.code,
      })
    })
  },[setRoomCodeData])
    // this api is called, returns whether in room or no
    // if in room, room code is fetched and response.json is returned which goes to data
    // and through this we get room code
    // we store room code in state of home page and that is used inside render method to determine whether or Not
    // redirect has to take place
    // once render method called once, this method runs asynchronously

  return (
    roomCodeData.roomCode ? (
      <Navigate replace to={`/room/${roomCodeData.roomCode}`} />
    ) : (
    <div>
      <Grid container spacing={3}>
        <Grid item xs={12} align="center">
          <Typography variant="h3" compact="h3">
            Music Party
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <ButtonGroup disableElevation variant="contained" color="primary">
            <Button color="primary" to="/join" component={Link}>
              Join a Room
            </Button>
            <Button color="secondary" to="/create" component={Link}>
              Create a Room
            </Button>
          </ButtonGroup>
        </Grid>
      </Grid>
      </div>
    )
  );
}

export default HomePage;