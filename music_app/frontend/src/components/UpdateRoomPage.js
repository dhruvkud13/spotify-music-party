import React, { Component } from 'react';
import { TextField, Button, Grid, Typography, FormHelperText,
            FormControl, Radio, RadioGroup, FormControlLabel}
        from '@material-ui/core';
import {withRouter} from './withRouter';
import { Collapse } from '@material-ui/core';
import { Alert } from '@material-ui/lab';


class UpdateRoomPage extends Component {

    constructor(props) {
        super(props);
        this.state = {
            guest_can_pause: this.props.guest_can_pause,
            votes_to_skip: this.props.votes_to_skip,
            roomCode: this.props.roomCode,
            msg: "",
            success:null
        };

        this.handleVotesChange = this.handleVotesChange.bind(this);
        this.handleGestCanPauseChange = this.handleGestCanPauseChange.bind(this);
        this.handleRoomButtonClicked = this.handleRoomButtonClicked.bind(this);
    }
    

    handleVotesChange(e) {
        this.setState({
            votes_to_skip: e.target.value
        });
    }

    handleGestCanPauseChange(e){
        this.setState({
            guest_can_pause: e.target.value === "true" ? true : false,
        });
    }

    handleRoomButtonClicked() {
        const requestOptions = {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json'},
            body: JSON.stringify({
                votes_to_skip: this.state.votes_to_skip,
                guest_can_pause: this.state.guest_can_pause,
                code: this.state.roomCode
            }),
        };
        
        fetch('/api/update-room', requestOptions)
            .then((response) => {
                if (response.ok) {
                    this.setState({
                        msg: "Room Updated Successfully!",
                        success:true
                    })
                } else {
                    this.setState({
                        msg: "Error Updating Room",
                        success:false
                    })
                }
            });
    }

    render() {
        return (
            <Grid container spacing={1}>
                <Grid item xs={12} align="center">
                    {/* collapse used to store error and success messages */}
                    <Collapse in={this.state.msg != ""} variant="h4">
                        {this.state.success ? (
                        <Alert
                            severity="success"
                            onClose={() => {
                                // to clear the success message
                                this.setState({msg: ""})}}
                        >
                            {this.state.msg}
                        </Alert>) : (
                        <Alert
                            severity="error"
                            onClose={() => {
                                this.setState({msg: ""})}}
                        >
                            {this.state.msg}
                        </Alert>)}
                    </Collapse>
                </Grid>
                <Grid item xs={12} align="center">
                    <Typography component="h4" variant="h4">
                        Modify Room: {this.state.roomCode}
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                    <FormControl component="fieldset">
                        <FormHelperText component={'span'}>
                            <div align='center'> guest control of playback </div>
                        </FormHelperText>
                        <RadioGroup row defaultValue={this.state.guest_can_pause.toString()} onChange={this.handleGestCanPauseChange}>
                            <FormControlLabel
                                value="true"
                                control={<Radio color="primary"/>}
                                label="Play/Pause"
                                labelPlacement="bottom"
                            />
                            <FormControlLabel
                                value="false"
                                control={<Radio color="secondary"/>}
                                label="No Control"
                                labelPlacement="bottom"
                            />
                        </RadioGroup>
                    </FormControl>
                </Grid>
                <Grid item xs={12} align="center">
                    <FormControl component={'span'}>
                        <TextField
                            required={true}
                            type="number"
                            onChange={this.handleVotesChange}
                            defaultValue={this.state.votes_to_skip}
                            inputProps={{
                                min: 1,
                                style: { textAlign: 'center' }
                            }}
                        />
                        <FormHelperText component={'span'} >
                            <div align='center'> Votes to skip</div>
                        </FormHelperText>
                    </FormControl>
                </Grid>
                <Grid item xs={12} align="center">
                    <Button color="primary" variant="contained" onClick={this.handleRoomButtonClicked}>
                        Modify
                    </Button>
                </Grid>
            </Grid>
        );
    }
}

export default withRouter(UpdateRoomPage);