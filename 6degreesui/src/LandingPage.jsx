import React, { useState, useEffect } from 'react'
import {useNavigate} from 'react-router-dom'
import axios from 'axios';
import Logo from './Logo.jsx'
import OtherLogo from './otherLogo.jsx'
import styled, {keyframes} from 'styled-components'
const LandingPageWrapper = styled.div`
    position: relative;
    width: 100%;
    height: 100vh;
`;

const TitleContainer = styled.div`
    position: absolute;
    top: 20%;  // You can adjust this to position your title vertically
    left: 50%;  // This will center the title horizontally
    transform: translate(-50%, -50%);  // This ensures the center of the title is at the position specified by top and left
    text-align: center;
    font-family: 'Montserrat', sans-serif;  // Make sure you've imported Orbitron font in your project
    font-weight: bold;
    font-size: 3em; // Adjust according to your preference
    color: #FFF;  // Change color as needed
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);  // This will give the text a shadow, adjust as needed
    z-index: 10;  // This ensures the title stays on top of the backdrop
    &:hover {
        opacity: .75;
    }
`;


const StyledLogo = styled.div`
    position: absolute;
    background-size: cover;
    top:14%;
    right:33.5%;  // You can adjust this to position your logo vertically  // This will center the logo horizontally  // This ensures the center of the logo is at the position specified by top and left
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
        background: linear-gradient(rgba(255,255,255,0.6), rgba(255,255,255,0.6)); // Change this to suit your needs
        z-index:1;
      }
`;
const StartButton = styled.button`
    position: absolute;
    top: 65%;
    left: 50%;
    transform: translate(-50%, -50%);
    padding: 10px 20px;
    font-size: 1.2em;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    background: #ff6347;
    color: white;
    transition: all 0.3s ease;
    width:15vw;
    height:4vw;
    z-index:1;
    &:hover {
        background: #ff4500;
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
                const url = 'http://127.0.0.1:5010/'
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
            <StyledLogo><Logo size="9vw"></Logo></StyledLogo>
            <TitleContainer>6degrees</TitleContainer>
            <StartButton onClick={goToGame}>Start</StartButton>
            
            </LandingPageWrapper>
           </> )}
        </div>
        
    )

};
export default LandingPage;