import React from 'react'
import ConnSidebar from "./ConnSidebar"
import Navbar from "./Navbar"

const Home: React.FC = () => {
  return (
    <div>
      <Navbar/>
      <ConnSidebar/>
    </div>
  )
}

export default Home