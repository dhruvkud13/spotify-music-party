import React,{useState,useEffect} from 'react'
import {useParams, useNavigate} from 'react-router-dom'
import { Grid, Button, Typography } from "@material-ui/core";
import UpdateRoomPage from './UpdateRoomPage';


const Room = () => {
    
        let roomCode = useParams().roomCode;
        const initialState = {
          votes_to_skip: 2,
          guest_can_pause: false,
          is_host: false,
          show_settings: false,
        //   spotify_authenticated: false,
        }
        const initialStateSpotify ={
            spotify_authenticated: null,
            // song: {}
          }

        // const[votesToSkip,setVotesToSkip] = useState(2);
        // const[guestCanPause,setGuestCanPause] = useState(false);
        // const[isHost,setIsHost] = useState(false);
        // const[showSettings,setShowSettings] = useState(false);
        
        let navigate= useNavigate();

        const [roomData, setRoomData] = useState(initialState);
        const [spotifyData, setSpotifyData] = useState(initialStateSpotify)

        useEffect(() => {
           fetch('/api/get-room' + '?code=' + roomCode)
           .then(response => {
            // this redirects user to home page coz room doesnt exist
            if (!response.ok) {
              navigate('/');
            }
            // return response.json();
            return response;
          })
           .then((response) => response.json())
            .then(data => {
                // console.log(data.json());
                setRoomData({
                  ...roomData, 
                  votes_to_skip: data.votes_to_skip,
                  guest_can_pause: data.guest_can_pause,
                  is_host: data.is_host,
                })
                // setVotesToSkip(data.votes_to_skip);
                // setGuestCanPause(data.guest_can_pause);
                // setIsHost(data.is_host);
                // console.log(data.json())
                return data;
            })
            .then(() => {
                authenticateSpotify();
              })
        },[roomCode,setRoomData])

        // this function doesnt send us back to room
        function LeaveRoom({}){
            const requestOptions = {
                method: "POST",
                headers: { "Content-Type": "application/json" },
            };
            fetch('/api/leave-room', requestOptions).then(
                (response)=>{navigate('/');}
            );    
        }

        let updateShowSettings = (value, reload) => {
            setRoomData({
              ...roomData,
              show_settings: value,
            })
            if (reload){
              window.location.reload();
            }
          }

          let renderSettings = () => {
            return(
              <Grid container spacing={1}>
                <Grid item xs={12} align="center">
                  <UpdateRoomPage
                    update={true}
                    votes_to_skip={roomData.votes_to_skip}
                    guest_can_pause={roomData.guest_can_pause}
                    roomCode={roomCode}
                  />
                </Grid>
                <Grid item xs={12} align="center">
                  <Button variant="contained" color="secondary" onClick={() => updateShowSettings(false, true)}>
                    Close
                  </Button>
                </Grid>
              </Grid>
            )
          }

          let renderSettingsButton = () => {
            return(
              <Grid item xs={12} align="center">
                <Button variant="contained" color="primary" onClick={() => updateShowSettings(true, false)}>
                  Settings
                </Button>
              </Grid>
            )
          }

        let authenticateSpotify=()=>{
            // useEffect(() => {
            fetch('/spotify/is-authenticated')
            .then((response)=>response.json())
            .then((data)=>{
                setSpotifyData({
                    ...spotifyData,
                    spotify_authenticated: data.is_authenticated,
                });
                console.log(data.is_authenticated);
            // now if user is not authenticated, we need to authenticate them
            if(!data.is_authenticated){
                fetch('/spotify/get-auth-url')
                .then((response)=>response.json())
                .then((data)=>{
                    // to take user to authentication url
                    window.location.replace(data.url);
                })
            }
            })
            // },[])
        }


    if (roomData.show_settings) {
        return renderSettings();
    }        
  return (
    <div>
        <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <Typography variant="h4" component="h4">
            Code: {roomCode}
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <Typography variant="h6" component="h6">
            Votes: {roomData.votes_to_skip}
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <Typography variant="h6" component="h6">
            Guest Can Pause: {roomData.guest_can_pause.toString()}
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <Typography variant="h6" component="h6">
            Host: {roomData.is_host.toString()}
          </Typography>
        </Grid>
        {roomData.is_host ? renderSettingsButton() : null}
        <Grid item xs={12} align="center">
          <Button
            variant="contained"
            color="secondary"
            onClick={LeaveRoom}
          >
            Leave Room
          </Button>
        </Grid>
      </Grid>
    </div>
  );
}


export default Room

// dramesjdel
// fsdbthklbm

{/* <h1>votes_to_skip={votesToSkip}</h1>
        <h1>guest_can_pause={guestCanPause.toString()}</h1>
        <h1>is_host={isHost.toString()}</h1>
        <h1>roomCode={roomCode}</h1> */}