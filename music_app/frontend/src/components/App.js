import React from 'react';
import {render} from 'react-dom';
// import '../../static/css/index.css';
import HomePage from './HomePage';
// // import RoomJoinPage from './RoomJoinPage';
// import CreateRoomPage from './CreateRoomPage';
import RoomJoinPage from "./RoomJoinPage";
import CreateRoomPage from "./CreateRoomPage";
import Room from "./Room";
import {
  BrowserRouter,
  Routes,
  Route,
  Link,
  Redirect,
} from 'react-router-dom';

const App = () => {
  return (
    <div className='center'>
       <BrowserRouter>
         <Routes>
           <Route path="/">
            <Route index element={<HomePage />} /> 
           </Route>
           <Route path="join" element={<RoomJoinPage />} />
           <Route path="create" element={<CreateRoomPage />} />
           <Route path='room/:roomCode' element={<Room />} />
         </Routes>
       </BrowserRouter>
    </div>
  )
}

export default App

const appDiv = document.getElementById('app');
render(<App />, appDiv);