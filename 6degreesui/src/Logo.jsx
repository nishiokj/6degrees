import React from 'react'
import logo from './images/logo10.png'

function Logo({size}) {
    return (
        <div>
            <img src={logo} alt="logo" style={{width:size, height:size}} />
        </div>
    )
}

export default Logo;