import { useState } from 'react'
import niwcLogo from './assets/niwc.png'
import './App.css'
import Search from './search'
function App() {
  return (
    <>
      <div>
        <img src={niwcLogo} className="logo" alt="Niwc Pacific logo" />
      </div>
      <h1>What's on your mind today?</h1>
      <Search />
    </>
  )
}

export default App
