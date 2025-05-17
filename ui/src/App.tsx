import './App.css';
import { Routes, Route } from 'react-router-dom';
import Home from "./home/Home"
import Workspace from './workspace/Workspace';
import {Theme} from "@radix-ui/themes"

function App() {
  
  return (
    <Theme>
      <div>
        <Routes>
          <Route path="/" element={<Home/>}/>
          <Route path="/workspace" element={<Workspace/>}/>
        </Routes>
      </div>
    </Theme>
  )
}

export default App
