import React from "react";
import './App.css';
import {BrowserRouter, Route, Routes} from 'react-router-dom';

import RegistrationPage from "./pages/register";
import LandingPage from "./pages/start";
import BasicPage from "./pages/basic";
import LoginPage from "./pages/login";
import ProfilePage from "./pages/profil";
import ImageCarousel from "./components/carusel";
import HomogenPage from "./pages/homogen";

function App() {

  return (

      <BrowserRouter>
          <Routes>
              <Route exact path="/start" element={<LandingPage />} />
              <Route path="/register" element={<RegistrationPage />} />
              <Route path="/login" element={<LoginPage />} />
              {/*<Route path="/" element={loggedIn ? <BasicPage component={<ImageCarousel />} /> : <LandingPage />} /> />*/}
              <Route path="/" element={<BasicPage component={<ImageCarousel />} />} />
              <Route path="/homogen" element={<BasicPage component={<HomogenPage />} />} />
              <Route path="/profile" element={<BasicPage component={<ProfilePage />} />} />
          </Routes>
      </BrowserRouter>

  );
}

export default App;
