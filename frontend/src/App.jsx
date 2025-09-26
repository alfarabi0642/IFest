import { Routes, Route } from "react-router-dom"
import { useNavigate } from "react-router-dom"

import Card from "./Card.jsx"
import Footer from "./Footer.jsx"
import Button from "./Button.jsx"
import Sidebar from './Sidebar.jsx'
import HomePage from "./Pages/HomePage.jsx"
import ContractList from "./Pages/ContractList.jsx"


function App() {
    return (
        <div className="flex">
            <Sidebar/>
            <div className="flex-1 ml-13">
                <Routes>
                    <Route path="/" element={<HomePage/>}/>
                    <Route path="/contracts" element={<ContractList/>} />
                </Routes>
            </div>
            <Footer/>
        </div>
    );

}

export default App