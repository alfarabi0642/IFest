import { Routes, Route } from "react-router-dom"

import Sidebar from './Sidebar.jsx'
import Details from "./Details.jsx"
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
                    {/*<Route path="/drafts" element={<ContractDraft/>} />
                    <Route path="/reviews" element={<ContractReview/>} />
                    <Route path="/notifications" element={<Notification/>} />
                    <Route path="/reports" element={<Reports/>} />
                    */}
                </Routes>
            </div>
            <Details/>
            {/* <Footer/> */ }
        </div>
    );

}

export default App