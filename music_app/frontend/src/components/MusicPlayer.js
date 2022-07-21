import React from 'react'
import { Grid, Typography, Card, IconButton, LinearProgress} from '@material-ui/core';
// import PlayArrowIcon from "@material-ui/icons/PlayArrow";
// import PauseIcon from "@material-ui/icons/Pause";
// import SkipNextIcon from "@material-ui/icons/SkipNext";
import { PlayArrow, SkipNext, SkipPrevious, Pause } from '@material-ui/icons';


const MusicPlayer = ({song}) => {

    const song_progress = (song.time / song.duration) * 100;

    const playSong=()=>{
        const requestOptions={
            method:'PUT',
            headers:{'Content-Type':'application/json'},
        }
        // console.log('hi');
        fetch('/spotify/play',requestOptions)
    }

    const pauseSong=()=>{
        const requestOptions={
            method:'PUT',
            headers:{'Content-Type':'application/json'},
        }
        // console.log('hiiiii');
        fetch('/spotify/pause',requestOptions)
    }

    const skipSongNext=()=>{
        const requestOptions={
            method:'POST',
            headers:{'Content-Type':'application.json'},
        }
        fetch('/spotify/skip-next',requestOptions)
    }

    const skipSongPrevious=()=>{
        const requestOptions={
            method:'POST',
            headers:{'Content-Type':'application.json'},
        }
        fetch('/spotify/skip-previous',requestOptions)
    }

  return (
    <div>
    <Card>
            <Grid container alignItems="center">
                <Grid item align="center" xs={4}>
                    <img src={song.image_url} height="100px" width="100px"/>
                </Grid>
                <Grid item align="center" xs={8}>
                    <Typography component="h5" variant="h5">
                        {song.title}
                    </Typography>
                    <Typography variant="subtitle1" color="textSecondary">
                        {song.artist}
                    </Typography>
                    <div>
                        {/* <IconButton onClick={() =>{skipSongPrevious()} }>
                            {song.votes_previous} / {song.votes_required}
                            <SkipPrevious />
                        </IconButton> */}
                        <IconButton onClick={() =>{song.is_playing? pauseSong(): playSong() }}>
                            {song.is_playing ? <Pause /> : <PlayArrow />}
                        </IconButton>
                        <IconButton onClick={() =>{skipSongNext()} }>
                            
                            <SkipNext />
                            {song.votes_next} /{" "} {song.votes_required}
                        </IconButton>
                    </div>
                    
                </Grid>
            </Grid>
            <LinearProgress variant="determinate" value={song_progress} />
        </Card>
    </div>
  )
}

export default MusicPlayer