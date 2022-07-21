import React from 'react'
import { Grid, Typography, Card, IconButton, LinearProgress} from '@material-ui/core';
// import PlayArrowIcon from "@material-ui/icons/PlayArrow";
// import PauseIcon from "@material-ui/icons/Pause";
// import SkipNextIcon from "@material-ui/icons/SkipNext";
import { PlayArrow, SkipNext, Pause } from '@material-ui/icons';

const MusicPlayer = ({song}) => {

    const song_progress = (song.time / song.duration) * 100;

  return (
    <div>
        {/* <Card>
        <Grid container alignItems="center">
          <Grid item align="center" xs={4}>
            <img src={song.image_url} height="100%" width="100%" />
          </Grid>
          <Grid item align="center" xs={8}>
            <Typography component="h5" variant="h5">
              {song.title}
            </Typography>
            <Typography color="textSecondary" variant="subtitle1">
              {song.artist}
            </Typography>
            <div>
              <IconButton>
                {song.is_playing ? <PauseIcon /> : <PlayArrowIcon />}
              </IconButton>
              <IconButton>
                <SkipNextIcon />
              </IconButton>
            </div>
          </Grid>
        </Grid>
        <LinearProgress variant="determinate" value={song_progress} />
      </Card>
    </div> */}
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
                        <IconButton onClick={()=>{}}>
                            {song.is_playing ? <Pause /> : <PlayArrow />}
                        </IconButton>
                        <IconButton onClick={()=>{}}>
                            {/* {song.votes} /{" "} {song.votes_to_skip} */}
                            <SkipNext />
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