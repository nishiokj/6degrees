import React, { useState, useEffect } from 'react'
import {useNavigate} from 'react-router-dom'
import axios from 'axios';
import WholeLogo from './WholeLogo.jsx'
import styled, {keyframes} from 'styled-components'
const LandingPageWrapper = styled.div`
    position: relative;
    width: 100%;
    height: 100vh;
`;

const LogoContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  top: 40%;
  left: 52%;
  transform: translate(-50%, -50%);
  width: 100%;
  z-index:10;
`;

// Usage example
// <LogoContainer>
//   <WholeLogo width="4vw" height="1vh" />
// </LogoContainer>

const TitleContainer = styled.div`
    position: absolute;
    top: 20%;  // You can adjust this to position your title vertically
    left: 43%;  // This will center the title horizontally

    text-align: center;
    font-family: 'IBM Plex Serif', serif;  // Make sure you've imported Orbitron font in your project
    font-weight: bold;
    font-size: 2.9vw; // Adjust according to your preference
    color: #FFF;  // Change color as needed
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);  // This will give the text a shadow, adjust as needed
    z-index: 10;  // This ensures the title stays on top of the backdrop
    &:hover {
        opacity: .75;
    }
`;


const StyledLogo = styled.div`
    position: absolute;
    background-size: cover;
    top:16.1%;
    right:38.3%;  // You can adjust this to position your logo vertically  // This will center the logo horizontally  // This ensures the center of the logo is at the position specified by top and left
    z-index: 3;  // This ensures the logo stays on top of the backdrop
    transform-origin: 50% 50%;
    filter:brightness(110%);
    &:hover {
        opacity: .75;
    }
`;

const Backdrop = styled.div`
    background: url(${props => props.src}) no-repeat center center/cover;
    width:100%;
    height:100%;
    position:absolute;
    z-index:1;
    &::after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)); // Change this to suit your needs
        z-index:1;
      }
`;
const StartButton = styled.button`
    position: absolute;
    top: 65%;
    left: 50%;
    transform: translate(-50%, -50%);
    padding: 10px 20px;
    font-size: 1.2vw;
    border: 2px solid white;  // Set border color to white
    border-radius: 5px;
    cursor: pointer;

    background: transparent;  // Set background to transparent
    color: white;
    transition: all 0.3s ease;
    width:15vw;
    height:4vw;
    z-index:1;

    &:hover {
        background: #FFF;  // Keep background transparent on hover
        color:#000;  // Change text color on hover
    }
`;
 

    const LandingPage = ({navigation}) => {
    const [background,setData]= useState("")
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();
    const goToGame = () => {
        navigate('./game')
    }
    useEffect(() => {
    
    
        const fetchBackground = async() => {
            try{
                const url = 'http://127.0.0.1:5011/'
                const response = await axios.get(url);
                setData(response.data.url)
            }catch(error){
                console.error('Error fetching background')
            }
            setLoading(false);
        }
        fetchBackground();
        
    }, [])
    return (
        
        <div>
            {loading ? (

                <p>Whats good</p> ) : ( <>
            <LandingPageWrapper>
            <Backdrop src={background}>
            </Backdrop>
            <StartButton onClick={goToGame}>Start</StartButton>
            <LogoContainer><WholeLogo  width="16vw" height="16vh"></WholeLogo></LogoContainer>
            </LandingPageWrapper>
           </> )}
        </div>
        
    )

};
export default LandingPage;