import React, { Fragment, useEffect, useRef, useState } from 'react';
import logo from './logo.svg';
import './App.css';
import NavBar from './layouts/main/NavBar';
import { Container } from 'semantic-ui-react';
import { Outlet, useLocation } from 'react-router-dom';
import Footer from './layouts/main/Footer';

function getWindowDimensions() {
  const { innerWidth: width, innerHeight: height } = window;
  return {
    width,
    height
  };
}
function App() {
  const location = useLocation();

  const [windowDimensions, setWindowDimensions] = useState(getWindowDimensions());
  const [footerTop, setfooterTop] = useState<number>();

  useEffect(() => {
    function handleResize() {
      setWindowDimensions(getWindowDimensions());
    }


    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [windowDimensions, footerTop, location]);
  return (
    <Fragment>
      <NavBar />
      <div style={{ marginBottom: "15px", minHeight: (windowDimensions.height - 372) + "px" }}>
        <Container fluid >

          <Outlet />
        </Container>
      </div>
      <Footer />
    </Fragment>
  );
}

export default App;
