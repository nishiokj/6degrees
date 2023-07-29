import React from 'react'
import logo from './images/logo3.png'

function Logo({size}) {
    return (
        <div>
            <img src={logo} alt="logo" style={{width:size, height:size}} />
        </div>
    )
}

export default Logo;